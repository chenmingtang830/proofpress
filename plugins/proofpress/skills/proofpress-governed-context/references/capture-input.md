# Prepare capture without guessing fields

Before the first submission, read `proofpress_get_capture_schema`. It returns
the current server's retrieval envelope, five locator variants, experiment
evidence and `qualifiers.experiment` schemas. No workspace mutation occurs.
On an older server without this tool, inspect the published tool input schema;
do not probe a write tool to discover its format. If it is insufficient, retain
the finding as a draft and report the missing schema.

## Selected file, PDF page or slide

1. Read only files selected for this task. Extract a bounded UTF-8 projection
   with an available document reader; record the actual reader/version/options
   in a non-empty JSON configuration file. For a page/slide, save only its text.
2. Copy one exact supporting excerpt into a UTF-8 quote file. Do not paraphrase
   or put a list/object in `quote`. Preserve whitespace; review the excerpt for
   private material before submission. Never send the whole source by default.
3. Resolve the directory containing this skill as `<skill-root>`. Build locally:

   ```sh
   python3 <skill-root>/scripts/prepare_evidence.py \
     --source /selected/study.pdf --text /selected/page-3.txt \
     --quote-file /selected/excerpt.txt --config /selected/extraction.json \
     --query 'Which observation supports this bounded finding?' \
     --adapter actual-reader --version actual-version --page 3
   ```

   Replace these paths and adapter details with actual selected inputs. The
   helper uses only Python's standard library and prints a payload; it does not
   submit, write files, install software, or use credentials. With no `--page`,
   it uses a unique quote's character offsets in the supplied text projection.
   It hashes source bytes, projection bytes and canonical extraction config
   separately. Keep the projection and extraction config available locally for
   reproduction. A hash records what was supplied; it does not prove extraction
   accuracy or permission to disclose it.
4. Submit the resulting object as **`payload`**, omitting `profile`. Both
   **`payload.evidence.quote`** and **`payload.evidence.locator`** are nested
   under `evidence`. A receipt's flattened `quote`/`locator` is an output format,
   not an input template. Bind the returned `evd_...` IDs in the claim proposal.

Use `page_span` for a slide (1-based slide number and that slide text digest).
`section_span` additionally requires a real section ID/digest **and page bounds**.
Never substitute a made-up digest, entire-file digest for a page digest, or
quote digest for a projection digest. The helper does not support cell or JSON
locators; follow the discovered schema and the actual extraction for those.

## Choose the profile honestly

Literature summaries and slide-backed observations normally omit `profile`.
The experiment profile represents an identifiable reproducible run, not every
finding about biology. It needs recorded `experiment_id`, `run_id`,
`model_revision`, `dataset_revision`, `environment_digest`, `config_digest`.
Do not fabricate these for a literature finding.

For an actual experiment claim, pass `profile: "experiment"` and:

```text
qualifiers.experiment = {
  schema_version: "proofpress/profile/experiment/v1",
  claim_kind: "finding" | "regression" | "no-change" | "failed-attempt" | "decision",
  experiment: { experiment_id, run_id, model_revision, dataset_revision,
                environment_digest, config_digest }
}
```

This is a field map, not a literal JSON payload. Use the returned schema for
closed fields and the additional failure record required for `failed-attempt`.
Submit source retrieval evidence before experiment metrics/table evidence;
use existing metric/table evidence for a derivation. Kernel checks of source
references, arithmetic and identity still apply. If required run metadata is
missing, keep a draft; do not drop the profile merely to get past an error.

## Recover from a rejection

Read the whole error and the discovered schema, correct all fields locally,
then retry. Retrieval envelope format and experiment claim qualifiers are
checked by MCP before the write; an error explicitly saying **before submission**
did not consume a key. Use that same key for the corrected request. Other
failures may have reached execution: read back the receipt/execution state.
After a timeout, retry only the identical request with the same key. Do not
repeatedly generate new keys or repeat mutations to infer a schema. A confirmed
terminal execution needs a deliberately corrected new attempt under the
server's idempotency rules. Report what remains incomplete.
