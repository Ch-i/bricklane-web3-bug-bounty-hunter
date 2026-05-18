"""`w3s suggest` — picks the best candidate to scrutinize next.

Given a populated candidate queue (after `w3s sweep`), this scores every
candidate by a weighted heuristic combining:

  * Stage-1 triage_score (the Opus-judged 1-10 quality)
  * payout_max_usd / estimated_hours  (ROI per hour of analysis)
  * urgency (how close is closes_at)
  * platform historical reliability (C4 > Sherlock > Cantina > Immunefi)
  * not-already-audited bonus

Returns the top N. Used to decide "which one do I scrutinize tonight?"
"""

from __future__ import annotations

import argparse
import math
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from rich.console import Console
from rich.table import Table

from harness import candidates as cand_store
from harness.candidates import Candidate

console = Console()


# Platform reliability priors (subjective, based on prior contest payouts +
# scope clarity). Higher = more likely to pay out for valid findings.
PLATFORM_PRIORS: dict[str, float] = {
    "code4rena": 1.00,
    "sherlock": 0.85,
    "cantina": 0.75,
    "immunefi": 0.65,  # bigger payouts but tougher scope
}


@dataclass
class Suggestion:
    candidate: Candidate
    score: float          # composite score (higher = better)
    components: dict      # per-factor breakdown for debugging
    reasoning: str        # human-readable summary


def _urgency_factor(closes_at: str | None) -> tuple[float, float | None]:
    """Map a closes_at ISO ts to an urgency score in [0, 1].

    Sweet spot: 3-7 days out — enough time to scrutinize + write up.
      <12h:   0.2 (too late)
      12-72h: 0.6 (rushed)
      3-7d:   1.0 (ideal)
      7-21d:  0.7 (still good)
      >21d:   0.4 (low urgency, may be deprioritized)
      None:   0.5 (unknown)
    """
    if not closes_at:
        return 0.5, None
    try:
        ct = datetime.fromisoformat(closes_at.replace("Z", "+00:00"))
    except ValueError:
        return 0.5, None
    hours = (ct - datetime.now(timezone.utc)).total_seconds() / 3600
    if hours < 0:
        return 0.0, hours  # closed already
    if hours < 12:
        return 0.2, hours
    if hours < 72:
        return 0.6, hours
    if hours < 168:  # 7d
        return 1.0, hours
    if hours < 504:  # 21d
        return 0.7, hours
    return 0.4, hours


def _payout_factor(payout_max_usd: int | None) -> float:
    """Log-scaled payout factor in [0, 1].

      0-1K:    0.1
      1K-10K:  0.3
      10K-100K:0.6
      100K-1M: 0.85
      >1M:     1.0
    """
    if not payout_max_usd or payout_max_usd <= 0:
        return 0.3  # unknown payouts get a moderate prior
    # log10 normalized: 1K=3, 10K=4, 100K=5, 1M=6, 10M=7
    log = math.log10(max(payout_max_usd, 100))
    return max(0.05, min(1.0, (log - 2) / 5))  # 100→0, 10M→1


def score_candidate(c: Candidate) -> Suggestion:
    """Compute the composite score + per-factor breakdown."""
    # Stage 1 score: 1-10, normalized to [0.1, 1.0]
    s1 = (c.triage_score / 10.0) if c.triage_score is not None else 0.5

    payout = _payout_factor(c.payout_max_usd)
    urgency, hours_left = _urgency_factor(c.closes_at)
    platform_prior = PLATFORM_PRIORS.get(c.platform, 0.5)

    # Penalize already-audited candidates: 0.4x if any audit_run_dirs present
    repeat_penalty = 0.4 if c.audit_run_dirs else 1.0

    # Skip candidates flagged as low-value by Stage 1
    skip_penalty = 0.2 if c.triage_status == "skip" else 1.0

    # Weighted geometric mean — gives a single floating-point score
    # higher weights = more important factors
    weights = {
        "stage1": 3.0,
        "payout": 2.0,
        "urgency": 1.5,
        "platform": 1.0,
    }
    factors = {
        "stage1": s1,
        "payout": payout,
        "urgency": urgency,
        "platform": platform_prior,
    }

    # weighted geometric mean
    log_sum = sum(w * math.log(max(0.01, v)) for v, w in zip(factors.values(), weights.values()))
    geo_mean = math.exp(log_sum / sum(weights.values()))
    composite = geo_mean * repeat_penalty * skip_penalty

    # Human reasoning
    parts = []
    if c.triage_score is not None:
        parts.append(f"stage1={c.triage_score:.1f}/10")
    else:
        parts.append("stage1=unranked")
    if c.payout_max_usd:
        parts.append(f"payout=${c.payout_max_usd:,}")
    if hours_left is not None:
        if hours_left < 0:
            parts.append("closed")
        elif hours_left < 24:
            parts.append(f"{int(hours_left)}h left")
        else:
            parts.append(f"{int(hours_left / 24)}d left")
    parts.append(f"platform={c.platform}")
    if c.audit_run_dirs:
        parts.append(f"already-audited({len(c.audit_run_dirs)})")
    if c.triage_status == "skip":
        parts.append("triage:skip")

    return Suggestion(
        candidate=c,
        score=composite,
        components=factors | {"repeat_penalty": repeat_penalty, "skip_penalty": skip_penalty,
                              "hours_left": hours_left},
        reasoning="  ".join(parts),
    )


def suggest_top_n(
    n: int = 5,
    *,
    platform: str | None = None,
    min_stage1: float | None = None,
    include_audited: bool = False,
    include_closed: bool = False,
) -> list[Suggestion]:
    """Return the top-N candidates by composite score."""
    candidates = cand_store.load_all()

    # Optional pre-filters
    if platform:
        candidates = [c for c in candidates if c.platform == platform]
    if min_stage1 is not None:
        candidates = [c for c in candidates if (c.triage_score or 0) >= min_stage1]
    if not include_audited:
        candidates = [c for c in candidates if not c.audit_run_dirs]
    if not include_closed:
        now = datetime.now(timezone.utc)
        kept = []
        for c in candidates:
            if not c.closes_at:
                kept.append(c)
                continue
            try:
                ct = datetime.fromisoformat(c.closes_at.replace("Z", "+00:00"))
                if ct > now:
                    kept.append(c)
            except ValueError:
                kept.append(c)
        candidates = kept

    scored = [score_candidate(c) for c in candidates]
    scored.sort(key=lambda s: s.score, reverse=True)
    return scored[:n]


def render_suggestions(suggestions: list[Suggestion]) -> None:
    if not suggestions:
        console.print("[yellow]No candidates match the filters. "
                      "Run `w3s sweep` first to populate the queue.[/yellow]")
        return
    t = Table(title="Top scrutinize candidates", show_lines=False)
    t.add_column("rank", justify="right")
    t.add_column("score", justify="right")
    t.add_column("id")
    t.add_column("platform")
    t.add_column("title", overflow="fold")
    t.add_column("factors")
    for i, s in enumerate(suggestions, 1):
        t.add_row(
            str(i),
            f"{s.score:.3f}",
            s.candidate.id,
            s.candidate.platform,
            s.candidate.title[:55],
            s.reasoning,
        )
    console.print(t)
    console.print()
    console.print("[dim]To scrutinize the top pick:[/dim]")
    if suggestions:
        console.print(f"  [bold cyan]w3s scrutinize --from-candidate {suggestions[0].candidate.id}[/bold cyan]")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-n", "--top", type=int, default=5,
                        help="How many suggestions to return.")
    parser.add_argument("--platform", help="Restrict to one platform.")
    parser.add_argument("--min-stage1", type=float, default=None,
                        help="Minimum Stage 1 triage score.")
    parser.add_argument("--include-audited", action="store_true",
                        help="Include candidates that already have audit_run_dirs.")
    parser.add_argument("--include-closed", action="store_true",
                        help="Include candidates whose closes_at is past.")
    args = parser.parse_args(argv)

    suggestions = suggest_top_n(
        args.top,
        platform=args.platform,
        min_stage1=args.min_stage1,
        include_audited=args.include_audited,
        include_closed=args.include_closed,
    )
    render_suggestions(suggestions)
    return 0


if __name__ == "__main__":
    sys.exit(main())
