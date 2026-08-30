---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-3-10
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0
title: Fee calculation occurs twice
vuln_class: []
---

# Fee calculation occurs twice

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md)_

---

**Description:** `SecuritizeOnRamp::subscribe, swap` calls `calculateDsTokenAmount` which performs an external call to calculate the fee:
```solidity
function calculateDsTokenAmount(uint256 _liquidityAmount) public view returns (uint256 dsTokenAmount, uint256 rate, uint256 fee) {
    fee = feeManager.getFee(_liquidityAmount);
    uint256 liquidityAmountExcludingFee = _liquidityAmount - fee;
```

Subsequently `BaseOnRamp::_executeLiquidityTransfer` is called which does it again:
```solidity
uint256 fee = feeManager.getFee(amount);
if (fee > 0) {
    liquidityToken.transfer(feeManager.feeCollector(), fee);
}
```

**Impact:** Duplicate storage reads of `feeManager` and duplicate external calls.

**Recommended Mitigation:** Calculate the fee once in top-level functions then pass it to child functions as an input parameter. In the `SecuritizeOnRamp::subscribe` example `fee` is already returned by `calculateDsTokenAmount` so it could be passed as input to `_executeLiquidityTransfer`, though this still results in multiple storage reads of `feeManager` which is not ideal - ideally `feeManager` would be read once from storage and passed to any child functions that require it as well.

**Securitize:** Acknowledged.
