---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-3-27
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-03-22T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md
tags:
- firm:recon-audits
- report:2025-03-22-apollon-report
title: '[L-28] `SwapPair` may revert on 0 transfer tokens'
vuln_class: []
---

# [L-28] `SwapPair` may revert on 0 transfer tokens

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Impact**
Certain tokens revert on a 0 amount transfer

The code also performs the check to prevent zero transfers in many parts, but in these 2 instances the check was missed

[Note that for OZ tokens, the check is not necessary](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/c304b6710b4b5fcf2a319ad28c36c49df6caef14/contracts/token/ERC20/ERC20.sol#L183-L211)

https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/SwapPair.sol#L234-L238

```solidity
    if (amount0InFee > 0) {
      uint amount0GovFee = (amount0InFee * swapOperations.getGovSwapFee()) / DECIMAL_PRECISION;
      _safeTransfer(token0, tokenManager.govPayoutAddress(), amount0GovFee); /// @audit 0 revert
      balance0 -= amount0GovFee;
    } 
```

https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/SwapPair.sol#L161-L163

```solidity
    // payout whats left
    _safeTransfer(token0, to, amount0 - burned0);
    _safeTransfer(token1, to, amount1 - burned1);
```

**Mitigation**

Check that each transfer is done only on non-zero amounts
