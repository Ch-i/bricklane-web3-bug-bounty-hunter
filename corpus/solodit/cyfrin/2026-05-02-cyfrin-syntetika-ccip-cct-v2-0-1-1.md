---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-02-cyfrin-syntetika-ccip-cct-v2-0-1-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-05-02T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-02-cyfrin-syntetika-ccip-cct-v2-0
title: '`HilToken::_update` inverted waiting-period check + permissionless `HilToken::requestTransfer`
  enables single-tx force-burn of any holder''s balance'
vuln_class: []
---

# `HilToken::_update` inverted waiting-period check + permissionless `HilToken::requestTransfer` enables single-tx force-burn of any holder's balance

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md)_

---

**Description:** Two coupled defects in the force-transfer / force-burn mechanism:

(a) `requestTransfer(from, to, amount)` is permissionless - any caller overwrites `$.pendingTransfer` with arbitrary values. Every other `request*` function in scope is admin-gated.

(b) The `_update` owner-bypass waiting-period check uses `>` instead of `<=`:

```solidity
require(
    $.pendingTransfer.to == to &&
        $.pendingTransfer.from == from &&
        $.pendingTransfer.amount == amount &&
        $.pendingTransfer.timestamp + $.requiredWaitingPeriod >
        block.timestamp,
    TransfersNotAllowed()
);
```

Same inversion pattern as on the `ownerMint` check; the check passes only while the window is still open - no actual delay.

**Impact:** Instant confiscation / destruction of any holder's tokens by the owner key. Griefing variant: because `requestTransfer` is permissionless, any user can overwrite the pending slot, bricking any legitimate owner force-transfer flow. Downstream: burned user cannot redeem baseAsset via Minter; permanent fund loss for affected users. For CCT future-work, the same path destroys bridge pool inventory.

**Recommended Mitigation:**
- Gate `requestTransfer` with `onlyRole(DEFAULT_ADMIN_ROLE)` or `onlyOwner`
- Flip the operator in `_update` to `<=` and add `$.pendingTransfer.timestamp != 0` guard

**Syntetika:** Fixed in commit [`0c8b861`](https://github.com/SyntetikaLabs/monorepo/commit/0c8b8615f7870104515f4e0333cc7527c87db642)

**Cyfrin:** Verified. Operator flipped and `requestTransfer` gated to `DEFAULT_ADMIN_ROLE`.
