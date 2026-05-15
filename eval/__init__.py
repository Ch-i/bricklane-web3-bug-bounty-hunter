"""Historical-exploit benchmark for the web3Sentinel audit harness.

Layout per entry (under ``eval/historical/`` or ``eval/c4-public/``):

    <name>/
        source/                  # minimal reproducible Solidity for the bug
        expected-finding.md      # YAML frontmatter + canonical bug description
        post-mortem.md           # links + summary (for human readers)

The ``expected-finding.md`` frontmatter drives scoring; see
``harness.eval_schema.ExpectedFinding``.
"""
