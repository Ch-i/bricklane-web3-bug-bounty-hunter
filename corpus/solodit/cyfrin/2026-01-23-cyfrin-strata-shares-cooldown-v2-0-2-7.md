---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-23-cyfrin-strata-shares-cooldown-v2-0-2-7
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-01-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-23-cyfrin-strata-shares-cooldown-v2-0
title: '`Tranche::maxWithdraw` can understate the max withdrawal for the `SharesCooldown`
  contract'
vuln_class: []
---

# `Tranche::maxWithdraw` can understate the max withdrawal for the `SharesCooldown` contract

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md)_

---

**Description:** When the owner is `SharesCooldown`, the CDO explicitly exempts it from exit fees / lockups:
```solidity
if (owner == address(sharesCooldown)) {
    return (TExitMode.ERC4626, 0, 0);
}
```

But `Tranche.maxWithdraw(owner)` derives `assetsNet` using `previewRedeem(sharesGross)`, and `previewRedeem` hardcodes `address(0)` as the owner when it queries exit conditions:

```solidity
function maxWithdraw(address owner) public view returns (uint256 assetsNet) {
    uint256 sharesGross = balanceOf(owner);
    assetsNet = Math.min(previewRedeem(sharesGross), cdo.maxWithdraw(address(this), owner));
}

function previewRedeem(uint256 sharesGross) public view returns (uint256 assetsNet) {
    (, uint256 fee,) = cdo.calculateExitMode(address(this), address(0));
    assetsNet = quoteRedeem(sharesGross, fee);
}
```

As a result, `maxWithdraw(address(sharesCooldown))` can be understated because `previewRedeem` may include an exit fee that does not apply to `SharesCooldown`.

**Recommended Mitigation:** In `maxWithdraw(owner)` take into account `SharesCooldown`

Alternatively, given that `SharesCooldown` only interacts with the redemption execution path (`Tranche::redeem`), consider documenting that `Tranche::maxWithdraw`, as well as `Tranche::previewRedeem` functions don't discount the fees exemption applied for the `SharesCooldown` contract.

**Strata:** Fixed in commit [4b49a00](https://github.com/Strata-Money/contracts-tranches/commit/4b49a00c772df2dbf66e0c2982d50ab2633c0fe2).

**Cyfrin:** Verified. `Tranche::maxWithdraw` and `Tranche::previewRedeem` inline comments now state that these functions are for public usage.
