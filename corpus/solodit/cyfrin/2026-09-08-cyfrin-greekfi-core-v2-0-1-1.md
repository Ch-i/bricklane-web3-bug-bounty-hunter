---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-08-cyfrin-greekfi-core-v2-0-1-1
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-09-08T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-08-cyfrin-greekfi-core-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-08-cyfrin-greekfi-core-v2-0
title: '`Receipt::setFee` has no upper bound, letting the Factory owner take 100%
  of a live market''s redemption proceeds'
vuln_class: []
---

# `Receipt::setFee` has no upper bound, letting the Factory owner take 100% of a live market's redemption proceeds

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-08-cyfrin-greekfi-core-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-08-cyfrin-greekfi-core-v2.0.md)_

---

**Description:** `Receipt::setFee` is callable by the Factory owner on any live market and stores `feeBps_` after a caller check only:

```solidity
/// @inheritdoc IReceipt
function setFee(uint64 feeBps_) external {
    if (msg.sender != address(factory) && msg.sender != factory.owner()) revert UnauthorizedCaller();
    feeBps = feeBps_;
    emit FeeUpdated(feeBps_);
}
```

`Factory::setFee` caps the creation-time default at 1000 bps, and `Factory::createOption2` seeds each new market from that capped value via `Receipt(receipt_).setFee(feeBps)`, but the per-market setter never re-applies the bound:

```solidity
/// @inheritdoc IFactory
function setFee(uint64 bps) external onlyOwner {
    if (bps > 1000) revert InvalidValue();
    feeBps = bps;
    emit Fee(bps);
}
```

`Receipt::_payout` computes the fee and the net payout on both legs of every redemption:

```solidity
function _payout(IERC20 token, address account, uint256 amount) internal returns (uint256 paid) {
    if (amount == 0) return 0;
    uint256 fee = Math.mulDiv(amount, feeBps, 10_000);
    if (fee > 0) feeAccrued[address(token)] += fee;
    paid = amount - fee;
    token.safeTransfer(account, paid);
}
```

At `feeBps == 10_000` the redemption succeeds after `Receipt::_redeem` has burned the holder's receipts, pays `0`, and credits the full gross amount to `feeAccrued`, which `Receipt::collectFees` pays to `factory.owner()`. Above `10_000` the subtraction underflows and every `Receipt::redeem, redeemFor` call on that market reverts until the owner lowers the fee. Pair-burn still works, but a writer who has sold their longs has no exit.

The `IReceipt::setFee` NatSpec acknowledges the missing cap:

```solidity
/// @notice Set this market's redeem fee. Callable by the creating Factory during deployment or
///         by the current Factory owner afterward. No cap or timelock is applied; values above
///         10000 bps make positive redemptions revert.
function setFee(uint64 feeBps_) external;
```

but the documented trust model says the opposite. The `IFactory::owner` NatSpec limits the owner's `setFee` reach to 10% and states it cannot touch a funded pool, and the README's "Trust boundaries" section and the `Factory` constructor note repeat the same guarantee:

```solidity
/// @notice The {Ownable} owner. Its reach into the protocol: {setFee} (≤ 10 %, used as the
///         default during market initialization; {IReceipt.setFee} can reprice a live market),
///         {IReceipt.sweep} (gated on `totalSupply() == 0`) and receiving {IReceipt.collectFees}.
///         It cannot touch a live position or a funded pool. `renounceOwnership` is disabled
///         ({OwnershipNotRenounceable}) because an ownerless factory would strand every accrued
///         fee and sweepable balance in every Receipt it ever created.
/// @return The current owner; never `address(0)`.
function owner() external view returns (address);
```

The code implements the weaker claim.

**Impact:** The Factory owner can take 100% of a live, funded market's redemption proceeds, or halt its redemptions entirely, with a single fee update - contradicting the documented "cannot touch a funded pool" and "<= 10%" owner-reach limits.

**Recommended Mitigation:** Enforce the same bound as `Factory::setFee` so the per-market rate can never exceed the documented 10%:

```solidity
error InvalidFee(); // add to IReceipt

function setFee(uint64 feeBps_) external {
    if (msg.sender != address(factory) && msg.sender != factory.owner()) revert UnauthorizedCaller();
    if (feeBps_ > 1000) revert InvalidFee();
    feeBps = feeBps_;
    emit FeeUpdated(feeBps_);
}
```


**GreekFi:** Fixed in [PR39](https://github.com/greekfi/contracts/pull/39)

**Cyfrin:** Verified. Receipt now enforces the same 1,000 bps fee ceiling as Factory.
