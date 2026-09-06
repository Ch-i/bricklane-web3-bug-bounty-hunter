---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-05-16-cyfrin-ethena-timelock-v2-0-1-2
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-05-16T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-16-cyfrin-ethena-timelock-v2.0.md
tags:
- firm:cyfrin
- report:2025-05-16-cyfrin-ethena-timelock-v2-0
title: Don't allow initially granting `EXECUTOR_ROLE` or `WHITELISTED_EXECUTOR_ROLE`
  to `address(0)`
vuln_class: []
---

# Don't allow initially granting `EXECUTOR_ROLE` or `WHITELISTED_EXECUTOR_ROLE` to `address(0)`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-05-16-cyfrin-ethena-timelock-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-16-cyfrin-ethena-timelock-v2.0.md)_

---

**Description:** The client has stated that initially they want the `EXECUTOR_ROLE` to be closed and that in the future they may open this up.

Hence `EthenaTimelockController::constructor` should revert if any elements in the `executors` or `whitelistedExecutors` input arrays is `address(0)`.

**Ethena:** Acknowledged; we prefer to keep the optionality here.
