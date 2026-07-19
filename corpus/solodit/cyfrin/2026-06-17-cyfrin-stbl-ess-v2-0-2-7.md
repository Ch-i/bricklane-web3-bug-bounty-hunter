---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-17-cyfrin-stbl-ess-v2-0-2-7
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-06-17T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-17-cyfrin-stbl-ess-v2-0
title: Each `STBL_Redemption_Core::iRedeem` lowers the pool's per-share value without
  compensating LPs, creating an incentive for LPs to front-run pending redeems
vuln_class: []
---

# Each `STBL_Redemption_Core::iRedeem` lowers the pool's per-share value without compensating LPs, creating an incentive for LPs to front-run pending redeems

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-17-cyfrin-stbl-ess-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md)_

---

**Description:** `STBL_Redemption_Core::iRedeem` (`contracts/redemption/STBL_Redemption_Core.sol:172`) splits the pool NFT, redeems the split slice through the issuer, and forwards the asset tokens to the redeemer. The pool NFT's `stableValueNet` falls by `_amt`, but `totalSupply` is never decremented. The per-LP withdrawable value is computed by `STBL_Redemption_Core::iFetchShare` (`contracts/redemption/STBL_Redemption_Core.sol:97`):

```solidity
return (userData[_user].stableValueNet * MetaData.stableValueNet) / totalSupply;
```

With `totalSupply` unchanged and `MetaData.stableValueNet` reduced, every LP's `STBL_Redemption_Core::iFetchShare` drops proportionally on every redeem. The LPs receive nothing in return: the redeemer's USST is burned inside `STBL_UT1e_Issuer::iWithdraw`, the pool gains no fee, and the asset tokens are forwarded directly to the redeemer.

An LP who sees a pending `STBL_Redemption::redeem` in the mempool is strictly better off calling `STBL_Redemption::withdraw(theirFullShare)` first to exit at the pre-redeem ratio, leaving the next-in-line LPs to absorb the loss.

**Impact:** LPs subsidize redemption liquidity without compensation, and the rational strategy is to race to exit before any visible redeem lands. The pool degenerates toward a death-spiral whenever a sizable redeem appears: the first LPs to withdraw escape at full value, the last LPs are left holding a depleted pool.

**Proof of Concept:**
1. LPs A and B each deposit a YLD NFT worth `100` `stableValueNet` via `STBL_Redemption::deposit`. Pool NFT now has `stableValueNet = 200`, `totalSupply = 200`. `STBL_Redemption_Core::iFetchShare(A) = STBL_Redemption_Core::iFetchShare(B) = 100`.
2. Redeemer C submits `STBL_Redemption::redeem(50)` to the mempool.
3. A observes C's pending transaction and front-runs with `STBL_Redemption::withdraw(100)`. At that moment `STBL_Redemption_Core::iFetchShare(A) = 100`, so the call succeeds and A exits with `100` of value. Pool NFT now `100`, `totalSupply = 100`.
4. C's `STBL_Redemption::redeem(50)` then executes against the smaller pool: pool NFT drops to `50`, `totalSupply` is left at `100`.
5. B's `STBL_Redemption_Core::iFetchShare(B) = (100 * 50) / 100 = 50`, half of what B deposited. B absorbs the entire `50` of redemption cost that A escaped.

**Recommended Mitigation:** Add a lock-in period on LP withdrawals inside `STBL_Redemption_Core::iWithdraw`. An LP that deposits at time `T` cannot call `STBL_Redemption::withdraw` until `T + lockDuration`, so they cannot react to a pending `STBL_Redemption::redeem` in the mempool and exit at the pre-redeem ratio. With the front-running path closed, the per-share value loss is absorbed evenly across the LP set the pool actually had at the time of the redeem.

To make the absorbed loss recoverable instead of permanent, route the yield that accrues to the pool NFT through `STBL_Redemption_Core::iClaimYield` regularly: yield distributed via `rewardIndex` raises every LP's claimable balance over time and offsets the per-share value the redeem removed. As long as accrued yield over the lock period meets or exceeds expected per-share redemption losses, LPs are not net worse off for staying in the pool.

Optionally cap each `STBL_Redemption::redeem` (and/or the cumulative redeemed amount in a rolling window) at a percentage of the pool NFT's `stableValueNet`, so no single redeem can move the per-share ratio by a large amount. A cap turns redemption pressure into a queue rather than a single discrete dilution event, making the lock-in period a smaller burden in practice.

**STBL:** Patched in commit [727cf6e](https://github.com/USD-Pi-Protocol/stbl-contracts-evm-redemptions/commit/727cf6e2b0d3d88a8db0c56ee4d284ee6573a18e).

**Cyfrin:** Resolved. The withdraw timelock and continuous yield routing reduce the front-run incentive and compensate LPs who stay in the pool. The protection depends on an operational guideline, since `_setTimelock` only enforces `_timelock != 0` and the admin must set a value high enough to be effective.



\clearpage
