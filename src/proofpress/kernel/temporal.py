"""Descriptive temporal metadata and explicit read-time windows (never authority)."""
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def temporal_metadata(row):
    q = row.get("qualifiers") or {}
    return {key: value for key, value in {
        "effective_date": q.get("effective_date"),
        "report_date": q.get("report_date"),
        "original_first_seen_at": q.get("original_first_seen_at"),
        "recorded_at": row.get("created_at"),
        "historical_reconstruction": q.get("historical_reconstruction", False),
        "expires_at": row.get("expires_at"),
    }.items() if value is not None}


def _instant(value, zone, *, date_end=False):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("time must be an ISO date or timezone-aware timestamp")
    if len(value) == 10:
        dt = datetime.strptime(value, "%Y-%m-%d").replace(tzinfo=zone)
        return dt + timedelta(days=1) if date_end else dt
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        raise ValueError("timestamp must include a timezone")
    return dt


def temporal_window(value):
    if value is None:
        return None
    if not isinstance(value, dict) or set(value) - {"since", "until", "known_before", "timezone"}:
        raise ValueError("invalid temporal_window fields")
    if not any(value.get(key) for key in ("since", "until", "known_before")):
        raise ValueError("temporal_window needs since, until or known_before")
    try:
        zone = ZoneInfo(value.get("timezone", "UTC"))
        bounds = {key: _instant(value[key], zone) for key in ("since", "until", "known_before") if key in value}
    except (ValueError, TypeError, ZoneInfoNotFoundError) as exc:
        raise ValueError("invalid temporal_window date or timezone") from exc
    if "since" in bounds and "until" in bounds and bounds["since"] >= bounds["until"]:
        raise ValueError("temporal_window since must be before until")
    return {"zone": zone, "bounds": bounds, "query": {**value, "timezone": str(zone)}}


def in_temporal_window(row, window):
    if window is None:
        return True
    q = row.get("qualifiers") or {}
    b, zone = window["bounds"], window["zone"]
    try:
        if "since" in b or "until" in b:
            # Never make a historical import appear new using created_at.
            effective = q.get("effective_date") or q.get("report_date")
            at = _instant(effective, zone)
            if "since" in b and at < b["since"]:
                return False
            if "until" in b and at >= b["until"]:
                return False
        if "known_before" in b:
            # Unknown first-known time is not point-in-time evidence. A date-only
            # value is conservatively treated as known by the end of that day.
            known = _instant(q.get("original_first_seen_at"), zone, date_end=True)
            if known > b["known_before"] or (len(q["original_first_seen_at"]) != 10 and known == b["known_before"]):
                return False
    except (ValueError, TypeError):
        return False
    return True
