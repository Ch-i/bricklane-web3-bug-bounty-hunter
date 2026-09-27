---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-07-04-hyperwave-stablecoin-oracle-and-off-chain-bot-3-3
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md
tags:
- firm:codespect
- report:2025-07-04-hyperwave-stablecoin-oracle-and-off-chain-bot
title: '[I-04] Missing Database Error Handling'
vuln_class: []
---

# [I-04] Missing Database Error Handling

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md)_

---

**Files:** [`atomic_request_repo.py`](https://github.com/SwellNetwork/hlp-internal-be/blob/c650a499023489bfa5d6ac027b28a940a3c44cdc/app/domain/boring_vault/repo/atomic_request_repo.py)

**Description:**

The `AtomicRequestRepo` class lacks error handling for database operations. All database calls (`get_by_id(...)`, `get_by_is_solved(...)`, `create(...)`) can throw SQL exceptions that will propagate unhandled to the calling code.

**Impact:**

- Silent failures — `get_by_id(...)` returns `None` for both “not found” and “database error” scenarios;
- Poor debugging — no logging of database errors;

**Recommendation:** Add comprehensive error handling with proper exception categorization:

```python
def create(self, request: AtomicRequest) -> AtomicRequest:
    try:
        with Session(self.db_engine) as session:
            session.add(request)
            session.commit()
            session.refresh(request)
            return request

    except IntegrityError as e:
        logger.error(f"Constraint violation creating request: {e}")
        if "duplicate key" in str(e).lower():
            raise ValueError("Request already exists")
        raise ValueError("Request violates business rules")

    except OperationalError as e:
        logger.error(f"Database connection error: {e}")
        raise RuntimeError("Database temporarily unavailable")

    except Exception as e:
        logger.error(f"Unexpected database error: {e}")
        raise
```

> Note: This code is provided as a reference example for the types of errors that should be handled.

**Status:** Acknowledged

**Client response:** Acknowledge. Silent failures will be handled in domain logic (e.g. `BoringVaultService` in `boring_vault.py`). For logging, there’s a global exception handler (FastAPI/celery built-in) which will catch and log the error, so we want to keep current version to make the code of `AtomicRequestRepo` short.
