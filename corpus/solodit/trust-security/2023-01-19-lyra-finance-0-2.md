---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-01-19-lyra-finance-0-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-01-19T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md
tags:
- firm:trust-security
- report:2023-01-19-lyra-finance
title: TRST-H-3 disordered fee calculated causes collateral changes to be inaccurate
vuln_class: []
---

# TRST-H-3 disordered fee calculated causes collateral changes to be inaccurate

_Section severity (from Solodit section header): High_  
_Audit firm: Trust Security_  
_Source report: [2023-01-19-Lyra Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md)_

---

**Description:**
`_increasePosition()` changes the Hedger’s GMX position by **sizeDelta** amount and 
**collateralDelta** collateral. There are two **collateralDelta** corrections - one for swap fees and 
one for position fees. Since the swap fee depends on up-to-date **collateralDelta**, it’s important 
to calculate it after the position fee, contrary to the current state. In practice, it may lead to 
the leverage ratio being higher than intended as **collateralDelta** sent to GMX is lower than it 
should be.
```solidity
      if (isLong) {
          uint swapFeeBP = getSwapFeeBP(isLong, true, collateralDelta);
           collateralDelta = (collateralDelta * (BASIS_POINTS_DIVISOR + swapFeeBP)) / BASIS_POINTS_DIVISOR;
      }
      // add margin fee
      // when we increase position, fee always got deducted from collateral
          collateralDelta += _getPositionFee(currentPos.size, sizeDelta, currentPos.entryFundingRate);
``` 

**Recommended Mitigation:**
Flip the order of `getSwapFeeBP()` and `_getPositionFee()`. 

**Team response:**
Fixed
