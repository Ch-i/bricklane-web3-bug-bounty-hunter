---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-04-10-tokentable-fractionalizer-and-sellnow-4-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-04-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-10-TokenTable-Fractionalizer-and-SellNow.md
tags:
- firm:codespect
- report:2025-04-10-tokentable-fractionalizer-and-sellnow
title: '[I-01] Missing check for transferability'
vuln_class: []
---

# [I-01] Missing check for transferability

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-04-10-TokenTable-Fractionalizer-and-SellNow.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-10-TokenTable-Fractionalizer-and-SellNow.md)_

---

**Files:** [SellNow.sol](https://github.com/EthSign/tokentable-sellnow-swap-evm/blob/eafe0d070b48a51e65394fc7b6f4eb3928f9af12/src/SellNow.sol#L48-L54)

**Description:**

The `SellNow` contract allows establishing a session between a buyer and a seller for an `actual` (i.e., `futureToken`). During session creation, several parameters are validated. However, to ensure consistency and prevent potential issues, the `createSession(...)` function could additionally verify whether the `futureToken` is transferable.

**Impact:** If a session is created with a non-transferable `futureToken`, the `SellNow` functionality will operate incorrectly.

**Recommendation(s):** Consider adding a check to ensure the `futureToken` is transferable before allowing session creation.

**Status:** Acknowledged

**Update from TokenTable:** will be handled off-chain
