---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-01-24-cyfrin-solidlyv3-3-4
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-01-24T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-24-cyfrin-solidlyV3.md
tags:
- firm:cyfrin
- report:2024-01-24-cyfrin-solidlyv3
title: Use multiple requires instead of a single one with multiple statements is better
  for gas consumption
vuln_class: []
---

# Use multiple requires instead of a single one with multiple statements is better for gas consumption

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-01-24-cyfrin-solidlyV3.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-24-cyfrin-solidlyV3.md)_

---

**Description:** Use multiple requires instead of a single one with multiple `&&` is better for gas consumption. The reason is because `require` is translated as [revert which does not consume gas](https://ethereum-org-fork.netlify.app/developers/docs/evm/opcodes) if it reverts. However `&&` consume gas. Therefore, opting for multiple require is more gas efficient than opting for a single one with multiple statements that mus be true.

```solidity
// SolidlyV3Pool.sol
116:    require(success && data.length >= 32);
127:    require(success && data.length >= 32);
278:    require(amount0 >= amount0Min && amount1 >= amount1Min, 'AL');
293:    require(amount0 >= amount0Min && amount1 >= amount1Min, 'AL');
391:     require(amount0FromBurn >= amount0FromBurnMin && amount1FromBurn >= amount1FromBurnMin, 'AL');
456:    require(amount0 >= amount0Min && amount1 >= amount1Min, 'AL');

// RewardsDistributor.sol
607:    require(success && data.length >= 32);
```

**Solidly:**
Acknowledged.
