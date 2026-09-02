#!/usr/bin/env python3
"""HTTP service for the single-owner Proofpress self-hosting reference."""
from __future__ import annotations

import argparse
from html import escape
import json
import os
from pathlib import Path
import secrets
import sqlite3
import sys
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlencode, urlparse

import proofpress_knowledge as knowledge
from proofpress_self_hosted.control_plane import HostedAuthError, HostedControlPlane


MAX_REQUEST_BYTES = 1024 * 1024
LOOPBACK_HOSTS = {"127.0.0.1", "::1", "localhost"}


def _status_for(envelope):
    if envelope.get("ok"):
        return HTTPStatus.OK
    code = envelope.get("error", {}).get("code")
    if code == "invalid_credential":
        return HTTPStatus.UNAUTHORIZED
    if code == "operation_forbidden":
        return HTTPStatus.FORBIDDEN
    if code in {"ledger_head_conflict", "idempotency_conflict"}:
        return HTTPStatus.CONFLICT
    if code in {"operation_rejected", "resource_not_found"}:
        return HTTPStatus.UNPROCESSABLE_ENTITY
    if code in {"operation_io_error", "idempotency_store_invalid",
                "idempotency_store_write_failed"}:
        return HTTPStatus.INTERNAL_SERVER_ERROR
    return HTTPStatus.BAD_REQUEST
