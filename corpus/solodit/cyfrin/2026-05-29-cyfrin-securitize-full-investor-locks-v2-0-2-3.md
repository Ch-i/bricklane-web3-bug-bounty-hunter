---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-29-cyfrin-securitize-full-investor-locks-v2-0-2-3
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-05-29T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-29-cyfrin-securitize-full-investor-locks-v2-0
title: '`ComplianceServiceLibrary::isMaximumHoldingsPerInvestorOk` uses exclusive
  `>=`; sibling minimums use inclusive `<`'
vuln_class: []
---

# `ComplianceServiceLibrary::isMaximumHoldingsPerInvestorOk` uses exclusive `>=`; sibling minimums use inclusive `<`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md)_

---

**Description:** The maximum-holdings-per-investor cap at `contracts/compliance/ComplianceServiceRegulated.sol:572-574` is evaluated as:

```solidity
function isMaximumHoldingsPerInvestorOk(uint256 _maximumHoldingsPerInvestor, uint256 _balanceOfInvestorTo, uint256 _value) internal pure returns (bool) {
    return _maximumHoldingsPerInvestor != 0 && _balanceOfInvestorTo + _value >= _maximumHoldingsPerInvestor;
}
```

The function returns `true` (reject the transfer) when the post-transfer balance would be greater than or equal to the configured maximum. The cap is therefore exclusive: an investor cannot end up holding exactly `maximumHoldingsPerInvestor`. The sibling minimum-holdings checks in the same library use strict-less-than comparisons (`balanceOfInvestorTo + _value < minimumHoldingsPerInvestor`), making those bounds inclusive (a balance equal to the configured minimum is permitted). The asymmetric reading of the configured numeric bound, inclusive at the minimum and exclusive at the maximum, contradicts the natural reading of the parameter name and is inconsistent with the protocol's own pattern at sibling sites. An issuer configuring `maximumHoldingsPerInvestor = N` who expects `N` to be allowable must instead configure `N + 1`.

**Files:**

`ComplianceServiceLibrary::isMaximumHoldingsPerInvestorOk` (`contracts/compliance/ComplianceServiceRegulated.sol`, lines 572-574)

**Recommended Mitigation:** Change the comparison to strict-greater-than to make the bound inclusive (matching the sibling minimum-holdings semantics):

```solidity
return _maximumHoldingsPerInvestor != 0 && _balanceOfInvestorTo + _value > _maximumHoldingsPerInvestor;
```

If the protocol intends an exclusive maximum (i.e., the cap value is the smallest forbidden balance), document the asymmetry in the configuration interface so the operator knows to set `maximumHoldingsPerInvestor = desiredCap + 1`.


**Securitize:** Acknowledged.

\clearpage
