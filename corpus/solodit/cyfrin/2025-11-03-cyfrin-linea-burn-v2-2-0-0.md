---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-03-cyfrin-linea-burn-v2-2-0-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-11-03T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-03-cyfrin-linea-burn-v2.2.md
tags:
- firm:cyfrin
- report:2025-11-03-cyfrin-linea-burn-v2-2
title: Tick spacing type mismatch in ExactInputSingleParams
vuln_class: []
---

# Tick spacing type mismatch in ExactInputSingleParams

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-03-cyfrin-linea-burn-v2.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-03-cyfrin-linea-burn-v2.2.md)_

---

**Description:** V3DexSwap uses the [Ramses V3 Swap Router](https://lineascan.build/address/0x8BE024b5c546B5d45CbB23163e1a4dca8fA5052A#code) to perform WETH to Linea swaps.

However, the ExactInputSingleParams struct definition passed as parameter to the exactInputSingle function differs between the V3DexSwap and the router contract.

**V3SwapDex definition**:
```solidity
struct ExactInputSingleParams {
    address tokenIn;
    address tokenOut;
    uint24 tickSpacing; <<
    address recipient;
    uint256 deadline;
    uint256 amountIn;
    uint256 amountOutMinimum;
    uint160 sqrtPriceLimitX96;
  }
```

**Ramses Router**:

```solidity
struct ExactInputSingleParams {
        address tokenIn;
        address tokenOut;
        int24 tickSpacing; <<
        address recipient;
        uint256 deadline;
        uint256 amountIn;
        uint256 amountOutMinimum;
        uint160 sqrtPriceLimitX96;
    }
```

As we can see, the tickSpacing member has differing types: uint24 and int24.

**Impact:** Due to this, if the POOL_TICK_SPACING value is greater than type(int24).max i.e. 8388607, the value will be interpreted incorrectly as a negative value in the router, causing a revert if such a pool does not exist or a successful swap through an unintended pool that anyone can frontrun create on RamsesV3.

**Proof of Concept:** **Recommended Mitigation:**
Update the struct definition in V3DexSwap to use int24 for tickSpacing instead of uint24.

**Linea:** Fixed at commit [be1cbc](https://github.com/Consensys/linea-monorepo/pull/1620/commits/be1cbce5ad0410d004e09d0f559522e4eee22daa)

**Cyfrin:** Verified.

\clearpage
