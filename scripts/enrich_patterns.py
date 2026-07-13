#!/usr/bin/env python3
"""Content enrichment pipeline — generates diagrams and video scripts for patterns.

Uses the locally authenticated Claude CLI to generate:
  1. Mermaid diagrams (architecture, attack flows, state machines)
  2. Manim video scripts (animated explainers)

Outputs are stored in content/{slug}/ and served via the API.

Usage:
    uv run python scripts/enrich_patterns.py [--slug specific-slug] [--all]
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from harness.autoresearch import get_topics_with_status, DOMAINS
from harness.corpus import get_entry, corpus_dir

CONTENT_DIR = REPO_ROOT / "content"
CONTENT_DIR.mkdir(exist_ok=True)

LOG_PATH = REPO_ROOT / "autoresearch-log.jsonl"


def log(msg, level="info", **extra):
    ts = datetime.now().strftime('%H:%M:%S')
    print(f"[{ts}] {msg}", flush=True)
    entry = {"ts": datetime.now().isoformat(), "level": level, "msg": msg, **extra}
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")


def get_synthesis_body(slug, synthesis_id):
    """Read the synthesis note body from the corpus."""
    # Try direct slug
    for sid in [synthesis_id, f"synthesis-{slug}"]:
        if not sid:
            continue
        entry = get_entry(sid)
        if entry:
            return entry.get("body", "") if isinstance(entry, dict) else ""
    # Fall back to reading the file directly
    for name in [slug, synthesis_id.replace("synthesis-", "") if synthesis_id else ""]:
        path = corpus_dir() / "synthesis" / f"{name}.md"
        if path.exists():
            return path.read_text()
    return ""


def generate_diagrams(slug, title, body, domain):
    """Use Claude CLI to generate Mermaid diagrams for a pattern."""
    out_dir = CONTENT_DIR / slug
    out_dir.mkdir(exist_ok=True)

    diagrams_file = out_dir / "diagrams.json"
    if diagrams_file.exists():
        log(f"  Diagrams already exist for {slug}, skipping", level="skip")
        return True

    prompt = f"""You are generating Mermaid.js diagrams for a web3 logic pattern library.

Pattern: {title}
Domain: {domain}

Here is the full synthesis note for this pattern:

{body[:6000]}

Generate exactly 3 Mermaid diagrams that explain this pattern visually:

1. **Architecture/Flow Diagram** — How the pattern works (flowchart or sequence diagram)
2. **Attack/Vulnerability Flow** — How the pattern can be exploited or fail (flowchart)
3. **Defense/Mitigation** — How to protect against the vulnerability (flowchart)

Output ONLY valid JSON in this exact format (no markdown, no code fences):
[
  {{"id": "architecture", "title": "How {title} Works", "type": "flowchart", "mermaid": "flowchart TD\\n    A[Start] --> B[Step]\\n    B --> C[End]"}},
  {{"id": "attack", "title": "Attack Vector", "type": "flowchart", "mermaid": "flowchart TD\\n    A[Attacker] --> B[Action]"}},
  {{"id": "defense", "title": "Defense Pattern", "type": "flowchart", "mermaid": "flowchart TD\\n    A[Check] --> B[Guard]"}}
]

Rules:
- Use flowchart TD (top-down) or sequenceDiagram
- Keep node labels SHORT (max 6 words)
- Use proper Mermaid syntax — quote labels with special chars
- Make diagrams specific to THIS pattern, not generic
- Use subgraph for grouping related steps
- Output raw JSON only, no explanation"""

    try:
        result = subprocess.run(
            ["claude", "-p", "--output-format", "text", "--max-turns", "1"],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(REPO_ROOT),
        )

        output = result.stdout.strip()
        # Try to extract JSON from output
        # Sometimes Claude wraps in ```json ... ```
        if "```" in output:
            parts = output.split("```")
            for p in parts:
                p = p.strip()
                if p.startswith("json"):
                    p = p[4:].strip()
                if p.startswith("["):
                    output = p
                    break

        diagrams = json.loads(output)
        diagrams_file.write_text(json.dumps(diagrams, indent=2))
        log(f"  ✓ Generated {len(diagrams)} diagrams for {slug}", level="diagram_done")
        return True

    except (subprocess.TimeoutExpired, json.JSONDecodeError, Exception) as e:
        log(f"  ✗ Diagram generation failed for {slug}: {e}", level="diagram_fail")
        return False


def generate_video_script(slug, title, body, domain):
    """Use Claude CLI to generate a Manim video script for a pattern."""
    out_dir = CONTENT_DIR / slug
    out_dir.mkdir(exist_ok=True)

    script_file = out_dir / "video_script.py"
    if script_file.exists():
        log(f"  Video script already exists for {slug}, skipping", level="skip")
        return True

    prompt = f"""You are generating a Manim Community Edition (manim) Python script that creates
an animated explainer video for a web3 logic pattern.

Pattern: {title}
Domain: {domain}

Key content from the synthesis note:
{body[:4000]}

Generate a complete, runnable Manim script that:
1. Shows a title card with the pattern name
2. Animates the core logic step-by-step (use Text, Arrow, Rectangle, VGroup)
3. Shows the attack/vulnerability flow with red highlights
4. Shows the defense pattern with green highlights
5. Ends with a summary of key takeaways

Use ONLY these Manim imports and classes:
- from manim import *
- Scene, Text, MathTex, Arrow, Rectangle, RoundedRectangle, VGroup, FadeIn, FadeOut, Write, Create, Transform, Indicate
- self.play(), self.wait()
- Use simple colors: RED, GREEN, BLUE, YELLOW, WHITE, GREY

The scene class should be named: PatternExplainer

Output ONLY the Python code, no explanation. The code must be syntactically valid."""

    try:
        result = subprocess.run(
            ["claude", "-p", "--output-format", "text", "--max-turns", "1"],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(REPO_ROOT),
        )

        output = result.stdout.strip()
        # Extract Python code if wrapped in code fences
        if "```python" in output:
            output = output.split("```python")[1].split("```")[0].strip()
        elif "```" in output:
            parts = output.split("```")
            for p in parts:
                p = p.strip()
                if "from manim" in p or "class " in p:
                    output = p
                    break

        if "from manim" not in output:
            log(f"  ✗ Video script for {slug} doesn't look like valid Manim code", level="video_fail")
            return False

        script_file.write_text(output)
        log(f"  ✓ Generated video script for {slug}", level="video_done")
        return True

    except (subprocess.TimeoutExpired, Exception) as e:
        log(f"  ✗ Video script generation failed for {slug}: {e}", level="video_fail")
        return False


def enrich_pattern(slug):
    """Generate all content for a single pattern."""
    topics = get_topics_with_status()
    topic = None
    for t in topics:
        if t["slug"] == slug:
            topic = t
            break
    if not topic:
        log(f"Topic not found: {slug}", level="error")
        return False
    if topic["status"] != "done":
        log(f"Skipping {slug} — not synthesized yet", level="skip")
        return False

    body = get_synthesis_body(slug, topic.get("synthesis_id"))
    if not body:
        log(f"No synthesis body found for {slug}", level="error")
        return False

    log(f"▶ Enriching: {topic['title']}", level="enrich_start", slug=slug, domain=topic["domain"])

    generate_diagrams(slug, topic["title"], body, topic["domain"])
    generate_video_script(slug, topic["title"], body, topic["domain"])

    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slug", type=str, help="Enrich a specific pattern by slug")
    parser.add_argument("--all", action="store_true", help="Enrich all synthesized patterns")
    parser.add_argument("--diagrams-only", action="store_true", help="Only generate diagrams")
    parser.add_argument("--videos-only", action="store_true", help="Only generate video scripts")
    args = parser.parse_args()

    if args.slug:
        enrich_pattern(args.slug)
    elif args.all:
        topics = get_topics_with_status()
        synthesized = [t for t in topics if t["status"] == "done"]
        log(f"Enriching {len(synthesized)} synthesized patterns", level="batch_start")
        for t in synthesized:
            enrich_pattern(t["slug"])
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
