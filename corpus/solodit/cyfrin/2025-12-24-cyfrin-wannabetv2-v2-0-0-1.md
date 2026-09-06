---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-wannabetv2-v2-0-0-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-wannabetv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-wannabetv2-v2-0
title: In `Bet::cancel` if one transfer reverts but the other succeeds, one users's
  tokens are permanently locked in the `Bet` contract
vuln_class: []
---

# In `Bet::cancel` if one transfer reverts but the other succeeds, one users's tokens are permanently locked in the `Bet` contract

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-wannabetv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-wannabetv2-v2.0.md)_

---

**Description:** `Bet::cancel` does this when refunding token transfers:
```solidity
try IERC20(b.asset).transfer(b.maker, makerRefund) {} catch {}
try IERC20(b.asset).transfer(b.taker, takerRefund) {} catch {}
```

But if one of the `transfer` calls reverts but the other succeeds, the transaction still successfully executes. This:
* moves the bet into the `CANCELLED` state
* keeps one user's tokens inside the `Bet` contract

**Impact:** For the user whose transfer reverted during the cancellation, there is no way for them to withdraw their tokens since `Bet::cancel` can't be called again, the `Bet` contract is immutable and there's no other functions that can rescue the tokens.

**Recommended Mitigation:** The simplest option is to remove the silent `catch` and revert the entire transaction if one of the `transfer` calls reverts; either both users are refunded or neither are.

A more complicated option is when cancelling a bet:
* update storage `Bet::makerStake,takerStake` to deduct the refunded amount if the transfer succeeded
* add a new function that allows the `maker` or `taker` of a given bet to withdraw their tokens if the bet has been cancelled but the `Bet` record shows they didn't receive a refund because the transfer failed.

**WannaBet:** Fixed in commit [f1750a9](https://github.com/gskril/wannabet-v2/commit/f1750a975346b1472ef3306db31f6fc7bd2db3b5).

**Cyfrin:** Verified.
