---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-wannabetv2-v2-0-1-3
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-wannabetv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-wannabetv2-v2-0
title: Aave rewards incentives lost as there is no way to claim them
vuln_class: []
---

# Aave rewards incentives lost as there is no way to claim them

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-wannabetv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-wannabetv2-v2.0.md)_

---

**Description:** When a bet uses an Aave pool, funds are supplied to Aave and can accrue [incentive rewards](https://aave.com/docs/aave-v3/aptos/smart-contracts/incentives), but the contracts provide no way to claim or forward these rewards (no integration with the Aave incentives controller and no generic sweep of reward tokens).

**Impact:** All Aave incentive rewards earned by bet positions are effectively lost/stranded, leading to missed revenue over time and potentially unrecoverable reward token balances.

**Recommended mitigation:**
Add a rewards-handling mechanism that can claim incentives via Aave’s incentives controller and route them according to the protocol’s economics, (treasury):
```solidity
function aave_claimRewards(address reward) external {
    address[] memory assets = new address[](1);
    assets[0] = _bet.asset;
    rewardsController.claimRewards(
        assets,
        type(uint256).max,
        _treasury,
        reward
    );
}
```

**WannaBet:** Acknowledged.

\clearpage
