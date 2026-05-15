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

**Discovered by:** {{ f.discovered_by }} &nbsp;|&nbsp; **Confidence:** {{ f.confidence }}
{%- if f.citations %} &nbsp;|&nbsp; **Citations:** {% for c in f.citations %}`{{ c }}`{% if not loop.last %}, {% endif %}{% endfor %}{%- endif %}

#### Description
{{ f.description }}

#### Impact
{{ f.impact }}

#### Recommendation
{{ f.recommendation }}

{%- if f.proof_of_concept %}

#### Proof of concept
```
{{ f.proof_of_concept }}
```
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


def render_markdown(report: AuditReport) -> str:
    env = Environment(
        loader=BaseLoader(),
        autoescape=False,
        trim_blocks=False,
        lstrip_blocks=False,
    )
    env.globals["severity_counts"] = _severity_counts
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
