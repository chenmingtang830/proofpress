import React from "react";
import { Button } from "./ui/button";
import { Disclosure, DisclosureContent, DisclosureTrigger } from "./ui/disclosure";
import { Table, TableBody, TableCaption, TableCell, TableHead, TableHeader, TableRow } from "./ui/table";
import "./evidence-source.css";
const Markdown = React.lazy(() => import("react-markdown"));

export type EvidenceDescription = {
  details: { filename: string; location: string; fields: { name: string; value: string }[] };
  actor?: string;
  created_at?: string;
  authority?: string;
};

export function sourceFilename(row: any, description?: EvidenceDescription): string | null {
  if (description?.details?.filename) return description.details.filename;
  const uri = row?.retrieval_receipt?.source?.uri || row?.source?.uri || row?.path;
  if (typeof uri !== "string" || uri.startsWith("urn:")) return null;
  const tail = uri.split(/[?#]/)[0].split(/[\\/]/).pop();
  if (!tail || !/\.[a-z\d]{1,8}$/i.test(tail)) return null;
  try { return decodeURIComponent(tail); } catch { return tail; }
}

function recordedLocation(locator: any): string {
  if (locator?.kind === "spreadsheet_cell") return `${locator.sheet}!${locator.cell}`;
  if (locator?.kind === "section_span") return `${locator.section_id} · pages ${locator.page_start}–${locator.page_end}`;
  if (locator?.kind === "page_span") return locator.page_start === locator.page_end ? `Page ${locator.page_start}` : `Pages ${locator.page_start}–${locator.page_end}`;
  if (locator?.kind === "text_span") return `Excerpt · characters ${locator.start}–${locator.end}`;
  if (locator?.kind === "json_pointer") return locator.value || "Whole JSON document";
  return "Source location not recorded";
}

function PriceRows({ records }: { records: any[] }) {
  const rows = records.slice(0, 100);
  return <div className="evidenceSourceTable" role="region" aria-label="Source price rows" tabIndex={0}>
    <Table>
      <TableCaption>Recorded source rows{records.length > rows.length ? ` · showing ${rows.length} of ${records.length}` : ""}. Returns are the supplied signed daily changes.</TableCaption>
      <TableHeader><TableRow><TableHead>Date</TableHead><TableHead>Symbol</TableHead><TableHead>Close</TableHead><TableHead>Daily change</TableHead><TableHead>Source cell</TableHead></TableRow></TableHeader>
      <TableBody>{rows.map((row, index) => <TableRow key={index}>
        <TableCell>{String(row.date ?? "Not recorded")}</TableCell>
        <TableCell>{String(row.symbol ?? "Not recorded")}</TableCell>
        <TableCell>{typeof row.close === "number" ? row.close.toLocaleString("en-US", {maximumFractionDigits: 4}) : "Not provided"}</TableCell>
        <TableCell>{typeof row.daily_return === "number" ? `${(row.daily_return * 100).toFixed(2)}%` : "Not provided"}</TableCell>
        <TableCell>{row.source_locator?.close_cell ? `${row.source_locator.sheet}!${row.source_locator.close_cell}` : "Not recorded"}</TableCell>
      </TableRow>)}</TableBody>
    </Table>
  </div>;
}

function StructuredExcerpt({ value }: { value: unknown }) {
  if (value === null) return <>Not provided</>;
  if (typeof value !== "object") return <>{String(value)}</>;
  if (Array.isArray(value)) return <ul>{value.map((item, index) => <li key={index}><StructuredExcerpt value={item} /></li>)}</ul>;
  return <dl className="evidenceSourceFields">{Object.entries(value).map(([key, item]) => <div key={key}><dt>{key.replaceAll("_", " ")}</dt><dd><StructuredExcerpt value={item} /></dd></div>)}</dl>;
}

export function RetrievalEvidence({ row, description, collapsible = false }: { row: any; description?: EvidenceDescription; collapsible?: boolean }) {
  const [expanded, setExpanded] = React.useState(false);
  const receipt = row.retrieval_receipt;
  const quote = String(receipt.quote || "No excerpt recorded.");
  let structured: any;
  try { structured = JSON.parse(quote); } catch { /* Keep the recorded Markdown excerpt. */ }
  const priceRows = Array.isArray(structured?.records) && structured.records.every((record: any) => record && typeof record === "object" && "symbol" in record && "close" in record);
  const fields = description?.details.fields || [];
  const location = description?.details.location || recordedLocation(receipt.locator);
  const canExpand = collapsible && (priceRows || quote.length > 420);
  return <div className="evidenceSource">
    <p className="evidenceSourceLocation">{location}</p>
    {fields.length > 0 && <dl className="evidenceSourceFields">{fields.map((field, index) => <div key={index}><dt>{field.name}</dt><dd>{field.value}</dd></div>)}</dl>}
    {!sourceFilename(row, description) && <p className="evidenceSourceMissing">The filename was not recorded with this evidence.</p>}
    <div className={`evidenceSourceExcerpt${canExpand && !expanded ? " isCollapsed" : ""}`}>
      {priceRows ? <PriceRows records={structured.records} /> : structured !== undefined ? <StructuredExcerpt value={structured} /> :
        <React.Suspense fallback={<p>Loading excerpt…</p>}><Markdown skipHtml allowedElements={["p", "strong", "em", "ul", "ol", "li", "a", "code", "blockquote", "br"]}
          components={{a: ({href, children}) => /^https?:\/\//i.test(href || "") ? <a href={href} target="_blank" rel="noreferrer" tabIndex={canExpand && !expanded ? -1 : undefined}>{children}</a> : <span>{children}</span>}}>
          {quote}
        </Markdown></React.Suspense>}
    </div>
    {canExpand && <Button type="button" variant="ghost" size="content" aria-expanded={expanded} onClick={() => setExpanded(!expanded)}>{expanded ? "Show less" : priceRows ? "Show all source rows" : "Show full excerpt"}</Button>}
    <Disclosure className="technicalDetails">
      <DisclosureTrigger>Technical receipt</DisclosureTrigger>
      <DisclosureContent>
        {description && <p>Source labels were supplied by {description.actor || "an agent"}{description.created_at ? ` on ${new Date(description.created_at).toLocaleDateString()}` : ""}. They do not modify the recorded evidence or authorize reuse.</p>}
        <pre>{JSON.stringify({evidence: row, ...(description ? {source_description: description} : {})}, null, 2)}</pre>
      </DisclosureContent>
    </Disclosure>
  </div>;
}
