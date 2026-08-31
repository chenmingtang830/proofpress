#!/usr/bin/env python3
"""Build deterministic image-PDF fixtures and source-bound structure gold."""
from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont, __version__ as pillow_version

GOLD_SCHEMA = "proofpress/document-extraction-ground-truth/v1"
PANEL_SCHEMA = "proofpress/document-extraction-ground-truth-panel/v1"


def digest(value: Any) -> str:
    data=json.dumps(value,sort_keys=True,separators=(",", ":")).encode()
    return "sha256:"+hashlib.sha256(data).hexdigest()


def file_digest(path: Path) -> str:
    return "sha256:"+hashlib.sha256(path.read_bytes()).hexdigest()


CASES = [
    ("dev-row-table", "development", "Annual Revenue", [["Year","Revenue","Tax"],["2022","$120,000","$18,000"],["2023","$135,500","$20,325"],["2024","$141,250","$21,188"]], "Prepared from audited schedule."),
    ("dev-column-table", "development", "Operating Margin", [["Metric","2022","2023","2024"],["Revenue","800","920","1,040"],["Cost","600","670","740"],["Margin","25%","27.17%","28.85%"]], "Values are stated in thousands."),
    ("dev-no-table", "development", "Payment Summary", None, "Invoice 1047 is due on 2026-09-15. The exact amount is $18,486."),
    ("dev-cross-page", "development", "Quarterly Schedule", [["Quarter","Units","Rate"],["Q1","125","$14.50"],["Q2","140","$14.50"],["Q3","155","$15.00"],["Q4","160","$15.00"]], "Schedule continues on the following page."),
    ("heldout-row-table", "heldout", "Cash Reconciliation", [["Period","Ledger","Bank"],["Jan","$48,200","$48,200"],["Feb","$51,075","$50,975"],["Mar","$49,640","$49,640"]], "Difference requires review."),
    ("heldout-column-table", "heldout", "Service Levels", [["KPI","April","May","June"],["Tickets","410","395","438"],["Resolved","389","381","420"],["SLA","94.88%","96.46%","95.89%"]], "Monthly operations report."),
    ("heldout-no-table", "heldout", "Contract Notice", None, "The renewal date is 2027-01-31 and the annual fee is $72,000."),
    ("heldout-cross-page", "heldout", "Payment Milestones", [["Milestone","Date","Amount"],["Signing","2026-10-01","$25,000"],["Delivery","2027-01-15","$40,000"],["Acceptance","2027-02-28","$35,000"]], "The final row appears on page two."),
]


def build_page(title: str, table: list[list[str]] | None, note: str,
               *, continuation_rows: set[int] | None = None) -> tuple[Image.Image, list[dict[str, Any]], list[dict[str, Any]]]:
    image=Image.new("RGB",(1400,1800),"white"); draw=ImageDraw.Draw(image); font=ImageFont.load_default(size=28)
    draw.text((100,90),title,fill="black",font=font)
    title_bbox=list(draw.textbbox((100,90),title,font=font))
    blocks=[{"text":title,"page":1,"bbox":title_bbox,"order":1}]
    tables=[]
    if table:
        x0,y0,row_h=100,240,75; widths=[360,300,300,300][:max(len(row) for row in table)]
        cells=[]
        for row_index,row in enumerate(table):
            cursor=x0
            for column_index,text in enumerate(row):
                width=widths[column_index]; box=[cursor,y0+row_index*row_h,cursor+width,y0+(row_index+1)*row_h]
                draw.rectangle(box,outline="black",width=3); draw.text((cursor+12,box[1]+20),text,fill="black",font=font)
                cells.append({"row":row_index,"column":column_index,"raw_text":text,"page":1,"bbox":box})
                cursor+=width
        table_box=[x0,y0,x0+sum(widths),y0+len(table)*row_h]
        tables.append({"id":"table-1","page":1,"bbox":table_box,"cells":table,"continuation_id":None})
        note_y=table_box[3]+80
    else: note_y=260
    draw.text((100,note_y),note,fill="black",font=font)
    blocks.append({"text":note,"page":1,"bbox":list(draw.textbbox((100,note_y),note,font=font)),"order":2})
    return image,blocks,tables


def build(root: Path) -> dict[str, Any]:
    root.mkdir(parents=True,exist_ok=True); sources=[]; gold_rows=[]
    for case_id,split,title,table,note in CASES:
        image,blocks,tables=build_page(title,table,note)
        images=[image]
        if "cross-page" in case_id and table:
            # Page two repeats the header and final data row. Gold explicitly
            # binds both physical tables to one continuation identity.
            second,second_blocks,second_tables=build_page(title+" — continued",[table[0],table[-1]],"End of schedule.")
            for block in second_blocks: block["page"]=2
            for row in second_tables: row["page"]=2; row["continuation_id"]=case_id+"-schedule"
            tables[0]["continuation_id"]=case_id+"-schedule"; images.append(second); blocks.extend(second_blocks); tables.extend(second_tables)
        pdf=root/(case_id+".pdf"); fixed_time=time.gmtime(0)
        images[0].save(pdf,"PDF",save_all=True,append_images=images[1:],resolution=144,
                       creationDate=fixed_time,modDate=fixed_time,producer="Proofpress fixture generator v1")
        content_digest=file_digest(pdf); uri="fixture://document-extraction/"+case_id+".pdf"
        source_id="source_"+content_digest[7:27]
        sources.append({"source_id":source_id,"split":split,"path":str(pdf),"uri":uri,
                        "media_type":"application/pdf","content_digest":content_digest})
        gold={"schema_version":GOLD_SCHEMA,"case_id":case_id,"split":split,
              "source_content_digest":content_digest,"blocks":blocks,"tables":tables}
        gold_path=root/(case_id+".gold.json"); gold_path.write_text(json.dumps(gold,indent=2,sort_keys=True)+"\n")
        gold_rows.append({"case_id":case_id,"split":split,"source_content_digest":content_digest,
                          "gold_digest":digest(gold),"gold_path":str(gold_path)})
    panel={"schema_version":PANEL_SCHEMA,"generator":"pillow-image-pdf/v1","pillow_version":pillow_version,
           "sources":sources,"gold":gold_rows,"development_count":4,"heldout_count":4,
           "downstream_task_outcome_access":False,"automatic_admission":False,"human_approval_required":True}
    panel_basis={"schema_version":PANEL_SCHEMA,"generator":panel["generator"],"pillow_version":pillow_version,
                 "sources":[{key:row[key] for key in ("source_id","split","media_type","content_digest")} for row in sources],
                 "gold":[{key:row[key] for key in ("case_id","split","source_content_digest","gold_digest")} for row in gold_rows]}
    panel["panel_digest"]=digest(panel_basis); (root/"panel.json").write_text(json.dumps(panel,indent=2,sort_keys=True)+"\n")
    execution={"schema_version":"proofpress/document-extraction-panel/v1","panel_digest":panel["panel_digest"],
               "development_count":4,"heldout_count":4,
               "sources":[{"source_id":row["source_id"],"split":row["split"],
                           "content_digest":row["content_digest"],"media_type":row["media_type"]} for row in sources],
               "routes":["current-canonical-native-representation","PaddlePaddle/PaddleOCR-VL-1.6"],
               "downstream_task_outcome_access":False,"automatic_admission":False,"human_approval_required":True}
    (root/"execution-panel.json").write_text(json.dumps(execution,indent=2,sort_keys=True)+"\n")
    return panel


def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument("--out",required=True,type=Path); args=parser.parse_args()
    panel=build(args.out); print(json.dumps({"ok":True,"panel_digest":panel["panel_digest"],"development":4,"heldout":4},sort_keys=True))


if __name__=="__main__": main()
