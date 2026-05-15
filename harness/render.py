"""Render an AuditReport to a markdown file (and sibling JSON artifacts)."""

from __future__ import annotations

import json
from pathlib import Path

from jinja2 import BaseLoader, Environment

from harness.schema import AuditReport

REPORT_TEMPLATE = """\
# Audit Report — {{ report.target }}

- **Target kind:** {{ report.target_kind }}
- **Timestamp:** {{ report.timestamp.isoformat() }}
- **Corpus snapshot:** `{{ report.corpus_snapshot }}`
{%- if report.model_versions %}
- **Models:**
  {%- for k, v in report.model_versions.items() %}
  - `{{ k }}`: {{ v }}
  {%- endfor %}
{%- endif %}

## Summary

{%- set counts = severity_counts(report.findings) %}
{%- set pocs = poc_summary(report.findings) %}
{%- if not report.findings %}
No findings.
{%- else %}
| Severity | Count |
| --- | ---: |
{%- for sev in ['Critical', 'High', 'Medium', 'Low', 'Informational', 'Gas'] %}
{%- if counts.get(sev) %}
| {{ sev }} | {{ counts[sev] }} |
{%- endif %}
{%- endfor %}

### Dynamic confirmation status

| PoC outcome | Count |
| --- | ---: |
{%- for status in ['reproduced', 'unconfirmed', 'compile-error', 'not-applicable', 'not-attempted'] %}
{%- if pocs.get(status) %}
| {{ poc_badge(status) }} | {{ pocs[status] }} |
{%- endif %}
{%- endfor %}

{% endif %}

## Static analyzer summary

{% for tool in report.static_tools -%}
- **{{ tool.tool }}** ({{ tool.version or 'no version' }}): {% if tool.succeeded %}OK{% else %}FAILED — {{ tool.error or 'unknown error' }}{% endif %}
{% endfor %}

{%- if report.findings %}
## Findings

{% for f in report.findings %}
### {{ loop.index }}. [{{ f.severity }}] {{ f.title }}
{%- if f.novel %} `[novel]`{% endif %}

{%- if f.location %}

**Location:**
{%- for loc in f.location %}
- `{{ loc.file }}:{{ loc.line_start }}{% if loc.line_end %}-{{ loc.line_end }}{% endif %}`
{%- endfor %}
{%- endif %}

**Discovered by:** {{ f.discovered_by }} &nbsp;|&nbsp; **Confidence:** {{ f.confidence }} &nbsp;|&nbsp; **PoC:** {{ poc_badge(f.poc_status) }}
{%- if f.citations %} &nbsp;|&nbsp; **Citations:** {% for c in f.citations %}`{{ c }}`{% if not loop.last %}, {% endif %}{% endfor %}{%- endif %}

#### Description
{{ f.description }}

#### Impact
{{ f.impact }}

#### Recommendation
{{ f.recommendation }}

{%- if f.proof_of_concept %}

#### Proof of concept (prose)
```
{{ f.proof_of_concept }}
```
{%- endif %}

{%- if f.foundry_poc %}

#### Foundry PoC

Runnable test: `{{ f.poc_artifacts.get("test_path", "(not scaffolded)") }}`
Status: **{{ f.poc_status }}**
{%- if f.poc_artifacts.get("stdout_log") %} &nbsp;|&nbsp; stdout: `{{ f.poc_artifacts["stdout_log"] }}`{% endif %}
{%- if f.poc_artifacts.get("stderr_log") %} &nbsp;|&nbsp; stderr: `{{ f.poc_artifacts["stderr_log"] }}`{% endif %}
{%- if f.foundry_poc.notes %}

> {{ f.foundry_poc.notes }}
{%- endif %}
{%- endif %}

---
{% endfor %}
{%- endif %}

{%- if report.model_disagreements %}
## Model disagreements

The Claude and Codex audit passes disagreed on the following points. These are
typically high-signal — one model spotted something the other missed, or they
interpreted the same code differently. Human review recommended.

{% for d in report.model_disagreements %}
### {{ loop.index }}. {{ d.topic }}

- **Claude:** {{ d.claude_position }}
- **Codex:**  {{ d.codex_position }}
{%- if d.reconciler_resolution %}
- **Reconciler resolution:** {{ d.reconciler_resolution }}
{%- endif %}
{% endfor %}
{%- endif %}
"""


def _severity_counts(findings) -> dict[str, int]:
    counts: dict[str, int] = {}
    for f in findings:
        counts[f.severity] = counts.get(f.severity, 0) + 1
    return counts


_POC_BADGES = {
    "reproduced": "✅ reproduced",
    "unconfirmed": "❓ unconfirmed",
    "compile-error": "⚠️ compile error",
    "not-applicable": "— n/a",
    "not-attempted": "— not attempted",
}


def _poc_badge(status: str) -> str:
    return _POC_BADGES.get(status, status)


def _poc_summary(findings) -> dict[str, int]:
    out: dict[str, int] = {}
    for f in findings:
        out[f.poc_status] = out.get(f.poc_status, 0) + 1
    return out


def render_markdown(report: AuditReport) -> str:
    env = Environment(
        loader=BaseLoader(),
        autoescape=False,
        trim_blocks=False,
        lstrip_blocks=False,
    )
    env.globals["severity_counts"] = _severity_counts
    env.globals["poc_badge"] = _poc_badge
    env.globals["poc_summary"] = _poc_summary
    template = env.from_string(REPORT_TEMPLATE)
    return template.render(report=report)


def write_report(report: AuditReport, run_dir: Path) -> Path:
    """Write report.md, static-tools.json, findings.json into ``run_dir``."""
    run_dir.mkdir(parents=True, exist_ok=True)

    report_path = run_dir / "report.md"
    report_path.write_text(render_markdown(report))

    (run_dir / "static-tools.json").write_text(
        json.dumps([t.model_dump() for t in report.static_tools], indent=2)
    )
    (run_dir / "findings.json").write_text(
        json.dumps([f.model_dump() for f in report.findings], indent=2)
    )
    (run_dir / "corpus-snapshot.txt").write_text(report.corpus_snapshot + "\n")

    return report_path
