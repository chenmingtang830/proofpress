export type KnowledgeRow = {
  id: string; label: string; state?: string; scope?: string; created_at?: string;
  applicability?: { title?: string; description?: string; when_relevant?: string[]; keywords?: string[]; validity_conditions?: string[] } | null;
};
export type KnowledgeSort = "newest" | "oldest" | "statement";
export function recordedIdentity(value: unknown, missing: string) {
  if (typeof value === "string" && value.trim()) return value;
  if (value && typeof value === "object") {
    const actor = value as { id?: unknown; name?: unknown };
    if (typeof actor.id === "string" && actor.id.trim()) return actor.id;
    if (typeof actor.name === "string" && actor.name.trim()) return actor.name;
  }
  return missing;
}
export function knowledgeTopic(row: KnowledgeRow) {
  return row.applicability?.title || row.scope || "";
}
// Input is the server's eligible projection. State labels are never an access filter.
export function selectKnowledge(rows: KnowledgeRow[], query: string, topic: string, sort: KnowledgeSort) {
  const terms = query.toLocaleLowerCase().trim().split(/\s+/).filter(Boolean);
  return rows.filter(row => {
    const card = row.applicability;
    const text = [row.label, row.id, row.scope, card?.title, card?.description, ...(card?.keywords || []), ...(card?.when_relevant || [])].join(" ").toLocaleLowerCase();
    return (!topic || knowledgeTopic(row) === topic) && terms.every(term => text.includes(term));
  }).sort((a, b) => {
    if (sort === "statement") return a.label.localeCompare(b.label) || a.id.localeCompare(b.id);
    const at = Date.parse(a.created_at || "");
    const bt = Date.parse(b.created_at || "");
    if (!Number.isFinite(at)) return Number.isFinite(bt) ? 1 : a.id.localeCompare(b.id);
    if (!Number.isFinite(bt)) return -1;
    return (sort === "oldest" ? at - bt : bt - at) || a.id.localeCompare(b.id);
  });
}
export function admissionRecord(receipt: any) {
  if (receipt.review?.decision === "admit") return receipt.review;
  return [...(receipt.history || [])].reverse().find(event => ["human_reviewed", "human_review"].includes(event.type) && event.decision === "admit") || null;
}
export function knowledgeDate(value?: string) {
  if (!value || !Number.isFinite(Date.parse(value))) return "Date not recorded";
  return new Date(value).toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" });
}
