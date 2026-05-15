---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-25-cyfrin-button-basis-trade-v2-0-2-3
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-09-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-25-cyfrin-button-basis-trade-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-25-cyfrin-button-basis-trade-v2-0
title: Decimal mismatch for tokens on HyperEVM and HyperCore
vuln_class: []
---

# Decimal mismatch for tokens on HyperEVM and HyperCore

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-25-cyfrin-button-basis-trade-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-25-cyfrin-button-basis-trade-v2.0.md)_

---

**Description:** The `transferToCore` function transfers a specified `amount` of the base asset from a pocket to HyperCore. However, it does not account for potential differences in decimal precision between the HyperEVM token and the HyperCore token. If the two systems use different decimal configurations (e.g., 6 decimals vs. 18 decimals), the transferred `amount` may represent a drastically different value on HyperCore than intended on HyperEVM. This can result in either loss of funds or inflation of balances, depending on the mismatch.

**Impact:** Agents could unintentionally transfer more or fewer tokens than expected due to mismatched decimals.

**Recommended Mitigation:** Consider introducing a decimal normalization mechanism when transferring between HyperEVM and HyperCore.

**Button:** Acknowledged. As there is not much on-chain info available for the HyperCore decimals we will solve this off-chain in the agent.
