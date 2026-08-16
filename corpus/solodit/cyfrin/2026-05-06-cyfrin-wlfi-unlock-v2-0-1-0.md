---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-06-cyfrin-wlfi-unlock-v2-0-1-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-05-06T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-06-cyfrin-wlfi-unlock-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-06-cyfrin-wlfi-unlock-v2-0
title: '`WorldLibertyFinancialRegistry::agentBulkInsertLegacyUsers` can be griefed
  by dust transfers when WLFI is transferable'
vuln_class: []
---

# `WorldLibertyFinancialRegistry::agentBulkInsertLegacyUsers` can be griefed by dust transfers when WLFI is transferable

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-06-cyfrin-wlfi-unlock-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-06-cyfrin-wlfi-unlock-v2.0.md)_

---

**Description:** In `WorldLibertyFinancialRegistry::agentBulkInsertLegacyUsers`, the operator supplies a list of `_users` and `_amounts`, and each row is checked with strict equality against the user's current WLFI balance.

```solidity
   function agentBulkInsertLegacyUsers(
        uint256 _expectedNonce,
        address[] calldata _users,
        uint256[] calldata _amounts,
        uint8[] calldata _categories
    ) external onlyWorldLibertyOwnerOrWhitelist(msg.sender) {
  ...
  for (uint256 i; i < _users.length; ++i) {
    ...
    if (WLFI.balanceOf(_users[i]) != _amounts[i]) {
        revert InvalidBulkInsertLegacyUserBalance(_users[i]);
    }
    ...
 }
}
```

The whole batch reverts if any single row fails this check. If WLFI is transferable at the time the operator runs this function, any external address can send a small amount of WLFI to any `_users[i]` to change its balance and force the batch to revert. The target user can also self grief by transferring their own balance out.

**Impact:** No funds are at risk and the nonce does not advance on revert, so the operator can retry. The result is wasted gas and a broken batching workflow: the operator must rebuild the snapshot, rebuild the arrays, and resubmit. A motivated griefer that watches the mempool can repeat this each time the operator tries to insert legacy users.

**Proof of Concept:** Assume WLFI is transferable and the operator has prepared a batch that includes `alice` with `_amounts[i] = 1000e18` matching `alice`'s current balance.

1. Operator submits the tx with a batch containing `alice`.
2. An attacker sees the pending tx in the mempool and frontruns it by sending `1 wei` of WLFI to `alice`.
3. The operator's tx executes. When the loop reaches `alice`, `WLFI.balanceOf(alice)` returns `1000e18 + 1` which is not equal to `_amounts[i]`.
4. The tx reverts with `InvalidBulkInsertLegacyUserBalance(alice)` and the full batch is lost.

The same outcome occurs if `alice` herself transfers any amount out before the tx mines.

**Recommended Mitigation:** Consider skipping the affected row instead of reverting the full batch, and emit an event so the operator can reconcile it later.

**WLFI:** Acknowledged. We don't plan on using this function anymore and to the extent we even need to, we'd rather it not fail silently for some users.
