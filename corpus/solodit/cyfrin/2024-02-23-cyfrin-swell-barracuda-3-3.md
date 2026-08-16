---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-02-23-cyfrin-swell-barracuda-3-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-02-23T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md
tags:
- firm:cyfrin
- report:2024-02-23-cyfrin-swell-barracuda
title: Use `totalReserves - rewardsInETH.unwrap()` rather than `_preRewardETHReserves
  - rewardsInETH.unwrap() + _newETHRewards` in `swETH::reprice`
vuln_class: []
---

# Use `totalReserves - rewardsInETH.unwrap()` rather than `_preRewardETHReserves - rewardsInETH.unwrap() + _newETHRewards` in `swETH::reprice`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-02-23-cyfrin-swell-barracuda.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md)_

---

**Description:** Both result in the same output but the first expression saves a `SUB` opcode. In addition the suggested modification results in simpler code which better reflects the intention of the invariant.

```diff
    // swETH::reprice
    uint256 totalReserves = _preRewardETHReserves + _newETHRewards;

    uint256 rewardPercentageTotal = swellTreasuryRewardPercentage +
      nodeOperatorRewardPercentage;

    UD60x18 rewardsInETH = wrap(_newETHRewards).mul(
      wrap(rewardPercentageTotal)
    );

    UD60x18 rewardsInSwETH = wrap(_swETHTotalSupply).mul(rewardsInETH).div(
-       wrap(_preRewardETHReserves - rewardsInETH.unwrap() + _newETHRewards)
+       wrap(totalReserves - rewardsInETH.unwrap())
    );
```

**Swell:** Fixed in commit [7db1874](https://github.com/SwellNetwork/v3-contracts-lst/commit/7db187409c7161d981b32d639e8b925fafc431a8).

**Cyfrin:**
Verified.
