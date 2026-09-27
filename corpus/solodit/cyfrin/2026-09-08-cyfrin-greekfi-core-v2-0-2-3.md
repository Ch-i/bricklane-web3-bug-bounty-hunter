---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-08-cyfrin-greekfi-core-v2-0-2-3
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-09-08T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-08-cyfrin-greekfi-core-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-08-cyfrin-greekfi-core-v2-0
title: '`Receipt::redeemFor` reverts an entire pre-deadline batch after the consideration
  pool is exhausted'
vuln_class: []
---

# `Receipt::redeemFor` reverts an entire pre-deadline batch after the consideration pool is exhausted

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-08-cyfrin-greekfi-core-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-08-cyfrin-greekfi-core-v2.0.md)_

---

**Description:** `Receipt::redeemFor` skips unauthorized and zero-balance holders, but forwards every other entry to `_redeem`. Before `exerciseDeadline`, collateral cannot be redeemed. Once earlier holders exhaust `consBacked`, the next non-zero holder therefore causes `ExerciseWindowOpen`, rolling back every earlier redemption in the transaction. This matches the documented atomic batch semantics: no holder loses a claim and the keeper can retry with a smaller batch, but the helper cannot provide best-effort progress and the failed attempt wastes gas.

**Recommended Mitigation:** If partial-progress batches are preferred, skip a holder when neither settlement leg is currently available. Keep the European pre-expiry revert and allow other `_redeem` failures to propagate:

```solidity
function redeemFor(address[] calldata holders) external nonReentrant {
    for (uint256 i = 0; i < holders.length; i++) {
        address h = holders[i];
        if (notAuthorized(h, msg.sender, Perm.REDEEM)) continue;

        uint256 balance = balanceOf(h);
        if (balance == 0) continue;

        if (isEuro() && block.timestamp < expirationDate()) {
            revert BeforeExerciseWindow();
        }
        if (consBacked == 0 && block.timestamp <= exerciseDeadline()) continue;

        _redeem(h, balance);
    }
}
```

Update the `redeemFor` NatSpec to state that entries with no currently available settlement leg are skipped.

**Greekfi:**
Accepted as intentional atomic batch behavior; no code change planned. IReceipt.redeemFor already states that only unauthorized and zero-balance holders are skipped and that any redemption revert rolls back the whole batch. test/Sweep.t.sol::test_RedeemFor_RevertAbortsWholeBatch pins the reported case.
