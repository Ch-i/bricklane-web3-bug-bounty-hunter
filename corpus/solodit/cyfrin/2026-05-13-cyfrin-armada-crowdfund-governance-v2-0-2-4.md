---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-2-4
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-05-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-13-cyfrin-armada-crowdfund-governance-v2-0
title: '`ArmadaRedemption::redeem` partial-sweep and per-asset share-zero forfeiture'
vuln_class: []
---

# `ArmadaRedemption::redeem` partial-sweep and per-asset share-zero forfeiture

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** `ArmadaRedemption::redeem` has an `anyPayout` guard that prevents ARM lock with zero return, but it fires on "`share > 0` for any one token" — partial-sweep still let value silently transfer from early to late redeemers:

- **Partial-sweep forfeiture** (`ArmadaRedemption.sol:150-169`): if some tokens in `tokens[]` have `available > 0` (already swept) and others have `available == 0` (sweep pending), the caller gets shares only from swept tokens. `anyPayout` passes; unswept tokens' shares are forfeited to later redeemers who arrive after the sweep lands.

The `REDEMPTION_DELAY` 7-day window (`:58,138`) gives sweepers time to run but does not force sweep ordering.

**Spec-Intent Gap:**

`specs/GOVERNANCE.md` §Wind-Down §Redemption mechanism Properties claims:

> **Sequential correctness.** Each redemption is calculated against the remaining assets and remaining circulating supply. **Early and late redeemers get the same pro-rata outcome**, with one caveat [revenue-lock releases].

Code achieves this only if all assets are swept before any redemption. The `REDEMPTION_DELAY` gives sweepers time but does not enforce sweep ordering.

**Impact:** Early redeemers lose shares of assets swept after their redemption; late redeemers receive more than pro-rata share of those assets.

**Recommended Mitigation:** Block silently-forfeiting paths — require a non-zero share for every token and ETH:

```solidity
for (uint256 i = 0; i < tokens.length; i++) {
    uint256 available = IERC20(tokens[i]).balanceOf(address(this));
    uint256 share = (available * armAmount) / circulating;
    require(share > 0, "ArmadaRedemption: dust share");
    SafeERC20.safeTransfer(IERC20(tokens[i]), msg.sender, share);
}
```

**Armada:** Fixed in commit [df67822](https://github.com/ship-armada/armada-poc/commit/df678220ad11c423aa096cb0efad62eef6658e0d).

**Cyfrin:** Verified.
