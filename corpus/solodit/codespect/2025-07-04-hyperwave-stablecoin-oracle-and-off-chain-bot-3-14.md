---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-07-04-hyperwave-stablecoin-oracle-and-off-chain-bot-3-14
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md
tags:
- firm:codespect
- report:2025-07-04-hyperwave-stablecoin-oracle-and-off-chain-bot
title: '[I-15] Consider refactoring textual SQL to ORM queries'
vuln_class: []
---

# [I-15] Consider refactoring textual SQL to ORM queries

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md)_

---

**Original severity:** Best Practices

**Files:** [`atomic_request_repo.py`](https://github.com/SwellNetwork/hlp-internal-be/blob/c650a499023489bfa5d6ac027b28a940a3c44cdc/app/domain/boring_vault/repo/atomic_request_repo.py#L19)

**Description:**

The `atomic_request_repo.py` file inconsistently combines ORM and raw SQL usage. This practice is generally discouraged, as it can lead to reduced readability, maintainability, and consistency across the codebase. Whenever possible, ORM should be preferred over raw SQL.

An example of raw SQL usage is found in the `get_by_is_solved(...)` function:

```python
def get_by_is_solved(self, is_solved: bool) -> List[AtomicRequest]:
    stmt = text(
        """
        SELECT * FROM atomic_requests
        WHERE is_solved = :is_solved
        """
    )
    stmt = stmt.bindparams(bindparam("is_solved"))
    with Session(self.db_engine) as session:
        result = session.exec(
            statement=stmt,
            params={"is_solved": is_solved},
        )
        rows = result.all()
        return [AtomicRequest(**dict(row._mapping)) for r
```

**Impact:** There is no direct security impact. However, this is noted as a best-practice finding.

**Recommendation:** Refactor the function to use ORM queries instead of raw SQL.

**Status:** Acknowledged

**Client response:** Acknowledged but will keep current version, respect author’s coding style.
