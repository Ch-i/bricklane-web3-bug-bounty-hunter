---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-03-cyfrin-linea-burn-v2-2-1-7
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-11-03T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-03-cyfrin-linea-burn-v2.2.md
tags:
- firm:cyfrin
- report:2025-11-03-cyfrin-linea-burn-v2-2
title: Burn and bridge mechanism can be delayed due to paused token bridge state
vuln_class: []
---

# Burn and bridge mechanism can be delayed due to paused token bridge state

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-03-cyfrin-linea-burn-v2.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-03-cyfrin-linea-burn-v2.2.md)_

---

**Description:** Contract RollupRevenueVault provides the BURNER_ROLE with the burnAndBridge() function. In this process, Linea tokens are meant to be bridged to L1 and burned there.

For bridging, the `tokenBridge` service is used, which can revert due to [it being paused](https://github.com/tree/contract-freeze-2025-10-12/blob/503a36c900419e9c6df00f5dad3d4c54d83f0578/linea/contracts/src/bridging/token/TokenBridgeBase.sol#L210)

**Impact:** Exeuction of the burn and bridge mechanism can be DOSed.

**Proof of Concept:** **Recommended Mitigation:**
Consider acknowledging the risk here and ensure appropriate measures are taken to handle such a scenario.

**Linea:** Acknowledged. This is acceptable, as we would then pause our burn job.

**Cyfrin:** Verified.
