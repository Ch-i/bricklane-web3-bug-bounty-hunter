---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-08-cyfrin-greekfi-core-v2-0-1-3
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
title: '`Option::exercise` uses the caller''s live balance, unsolicited transfers
  can revert the call near expiry'
vuln_class: []
---

# `Option::exercise` uses the caller's live balance, unsolicited transfers can revert the call near expiry

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-08-cyfrin-greekfi-core-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-08-cyfrin-greekfi-core-v2.0.md)_

---

**Description:** The no-argument `Option::exercise` exercises the caller's full live balance. Anyone can transfer Options to the holder before the transaction. If the holder approved only enough consideration for their original balance, the added Options increase the pull in `Receipt::exercise`, causing the call to revert.

**Impact:** An attacker can delay exercise for the cost of the transferred Options. The holder can retry with `exercise(uint256)`, but a last-minute revert may make them miss the exercise window and lose the option's in-the-money value.

**Recommended Mitigation:** Document that the no-argument overload uses an externally inflatable balance and recommend `exercise(uint256)` for deadline-sensitive calls. Alternatively, make it best-effort by capping the exercise to the consideration the holder can currently spend:

```solidity
uint256 optionBalance = balanceOf(msg.sender);
IERC20 cons = receipt.consideration();
uint256 budget = Math.min(
    cons.allowance(msg.sender, address(FACTORY)),
    cons.balanceOf(msg.sender)
);
uint256 amount = receipt.toConsideration(optionBalance, true) <= budget
    ? optionBalance
    : receipt.toCollateral(budget);
exerciseFor(msg.sender, amount);
```

Return the exercised amount and document that this overload may partially exercise.

**GreekFi:** Fixed in [PR46](https://github.com/greekfi/contracts/pull/46)

**Cyfrin:** Verified. The no-argument exercise documentation now warns that unsolicited transfers can increase the live balance and recommends the fixed-amount overload for deadline-sensitive calls.

\clearpage
