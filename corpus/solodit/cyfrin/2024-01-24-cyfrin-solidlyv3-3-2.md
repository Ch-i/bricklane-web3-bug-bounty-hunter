---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-01-24-cyfrin-solidlyv3-3-2
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-01-24T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-24-cyfrin-solidlyV3.md
tags:
- firm:cyfrin
- report:2024-01-24-cyfrin-solidlyv3
title: Prefer `++x` to `x++`
vuln_class: []
---

# Prefer `++x` to `x++`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-01-24-cyfrin-solidlyV3.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-24-cyfrin-solidlyV3.md)_

---

**Description:** Prefer `++x` to `x++`:

File: `TickBitmap.sol`
```solidity
48:        if (tick < 0 && tick % tickSpacing != 0) compressed--; // round towards negative infinity
```

File: `SolidlyV3Pool.sol`
```solidity
965:            if (amount0 == poolFees.token0) amount0--; // ensure that the slot is not cleared, for gas savings
```

File: `SolidlyV3Pool.sol`
```solidity
970:            if (amount1 == poolFees.token1) amount1--; // ensure that the slot is not cleared, for gas savings
```

File: `FullMath.sol`
```solidity
120:            result++;
```

**Solidly:**
Acknowledged.
