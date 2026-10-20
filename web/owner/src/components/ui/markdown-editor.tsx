import React from "react";
const ReactMarkdown = React.lazy(()=>import("react-markdown"));
import { Button } from "./button";
import { Textarea } from "./textarea";

type MarkdownEditorProps = {
  label: string;
  value: string;
  onChange: (value: string) => void;
  maxLength?: number;
  placeholder?: string;
  className?: string;
};

/** A plain Markdown source editor with a safe, optional reading view. */
export function MarkdownEditor({label,value,onChange,maxLength,placeholder,className=""}:MarkdownEditorProps) {
  const [preview,setPreview] = React.useState(false);
  return <div className={`markdownEditor ${className}`}>
    <div className="markdownEditorBar" role="group" aria-label={`${label} view`}>
      <span>{label}</span><div>
        <Button type="button" size="content" variant="ghost" aria-pressed={!preview} onClick={()=>setPreview(false)}>Edit</Button>
        <Button type="button" size="content" variant="ghost" aria-pressed={preview} onClick={()=>setPreview(true)}>Preview</Button>
      </div>
    </div>
    {preview ? <div className="markdownPreview" role="region" aria-label={`${label} preview`} tabIndex={0}>
      {value.trim() ? <React.Suspense fallback={<p role="status">Loading preview…</p>}><ReactMarkdown skipHtml components={{img:({alt})=><span>{alt || "Image omitted"}</span>}}>{value}</ReactMarkdown></React.Suspense> : <p className="markdownEmpty">Nothing to preview yet.</p>}
    </div> : <Textarea aria-label={label} value={value} maxLength={maxLength} placeholder={placeholder} onChange={e=>onChange(e.target.value)} />}
  </div>;
}
