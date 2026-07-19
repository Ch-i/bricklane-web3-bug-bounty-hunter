---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-0-5
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: '`PaymentSettler` can change `stablecoin` but `RemoraToken` can''t resulting
  in corrupted state with DoS for core functions'
vuln_class: []
---

# `PaymentSettler` can change `stablecoin` but `RemoraToken` can't resulting in corrupted state with DoS for core functions

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** `RemoraToken` has a `stablecoin` member with a comment that indicates it must match `PaymentSettler`:
```solidity
address public stablecoin; //make sure same stablecoin is used here that is used in payment settler
```

But in the updated code there is no way to update `RemoraToken::stablecoin`; previously `DividendManager` which `RemoraToken` inherits from had a `changeStablecoin` function but this was commented out with the introduction of `PaymentSettler`.

`PaymentSettler` has a `stablecoin` member and a function to change it:
```solidity
address public stablecoin;

function changeStablecoin(address newStablecoin) external restricted {
    if (newStablecoin == address(0)) revert InvalidAddress();
    stablecoin = newStablecoin;
}
```

**Impact:** When `PaymentSettler` changes its `stablecoin` it will now be different to `RemoraToken::stablecoin` which can't be changed, corrupting the state causing key functions to revert.

**Proof Of Concept:**
```solidity
function test_changeStablecoin_inconsistentState() external {
    address newStableCoin = address(new Stablecoin("USDC", "USDC", 0, 6));

    // change stablecoin on PaymentSettler
    paySettlerProxy.changeStablecoin(newStableCoin);
    assertEq(paySettlerProxy.stablecoin(), newStableCoin);

    // now inconsistent with RemoraToken
    assertEq(remoraTokenProxy.stablecoin(), address(stableCoin));
    assertNotEq(paySettlerProxy.stablecoin(), remoraTokenProxy.stablecoin());

    // no way to update RemoraToken::stablecoin
}
```

**Recommended Mitigation:** Enforce that `RemoraToken` and `PaymentSettler` must always refer to the same `stablecoin`. When implementing this consider our other findings where changing the `stablecoin` to one with different decimals corrupts protocol accounting.

The simplest solution may be to remove `stablecoin` from `RemoraToken` completely and have `PaymentSettler` perform all the necessary transfers.

**Remora:** Fixed in commit [ced21ba](https://github.com/remora-projects/remora-smart-contracts/commit/ced21ba9758b814eb48a09a5e792aa89cc87e8f5) by removing `stablecoin` from `RemoraToken`, moving the transfer fee logic into `PaymentSettler` and having `RemoraToken` call `PaymentSettler::settleTransferFee`.

**Cyfrin:** Verified.

\clearpage
