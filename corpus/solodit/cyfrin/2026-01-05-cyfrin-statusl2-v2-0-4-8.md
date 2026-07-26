---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-4-8
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-01-05T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-05-cyfrin-statusl2-v2-0
title: Slashing won't work after enabling emergency mode
vuln_class: []
---

# Slashing won't work after enabling emergency mode

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-05-cyfrin-statusl2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md)_

---

**Description:** Misbehaving users must be slashed via `RLN.sol`, it calls `Karma::slash`. This function iterates over reward distributors and calls `redeemRewards` which is expected to not revert. However `StakeManager::redeemRewards` reverts in emergency mode:
```solidity
    function redeemRewards(address account) external onlyNotEmergencyMode whenNotPaused returns (uint256) {
```

**Recommended Mitigation:** You should remove reward distributor after enabling it's emergency mode. Then retrieve rewards snapshot and mint lost Karma balances directly to users.

**StatusL2:** Fixed in [a5d51d5](https://github.com/status-im/status-network-monorepo/commit/a5d51d55f07dbbed4e3edd34042e0989d0e29f5a).

**Cyfrin:** Verified.

\clearpage
