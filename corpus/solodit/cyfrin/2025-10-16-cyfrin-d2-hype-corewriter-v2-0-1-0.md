---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-16-cyfrin-d2-hype-corewriter-v2-0-1-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-10-16T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-d2-hype-corewriter-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-16-cyfrin-d2-hype-corewriter-v2-0
title: '`nonReentrant` not the first modifier'
vuln_class: []
---

# `nonReentrant` not the first modifier

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-16-cyfrin-d2-hype-corewriter-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-d2-hype-corewriter-v2.0.md)_

---

**Description**
Across `Hype_Module`, `nonReentrant` is listed after `onlyRole(EXECUTOR_ROLE)` on external functions. In Solidity, modifiers are applied left-to-right, and the first modifier becomes the outermost wrapper. For consistent defense-in-depth, `nonReentrant` should be first so it also guards any logic within subsequent modifiers (present or future), minimizing the risk that a modifier could perform state changes or external calls before the reentrancy guard is set.

Consider changing the functions to have `nonReentrant` as the first modifier.

**D2:** Fixed in commit [`c5aeb40`](https://github.com/d2sd2s/d2-contracts/commit/c5aeb405bc5c9b4cd2a173eacf6b8ebbd8890ea8)

**Cyfrin:** Verified.
