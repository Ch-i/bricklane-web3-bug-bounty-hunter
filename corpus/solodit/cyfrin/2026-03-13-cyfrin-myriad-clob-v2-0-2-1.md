---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-2-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-myriad-clob-v2-0
title: '`AdminRegistry` inherited `grantRole`/`revokeRole` bypass the two-step transfer
  guard'
vuln_class: []
---

# `AdminRegistry` inherited `grantRole`/`revokeRole` bypass the two-step transfer guard

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-myriad-clob-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md)_

---

**Description:** `AdminRegistry` inherits from OpenZeppelin `AccessControl`, which exposes public `grantRole` and `revokeRole` functions callable by the role admin (which for `DEFAULT_ADMIN_ROLE` is itself). A current admin can call `grantRole(DEFAULT_ADMIN_ROLE, newAdmin)` and then `revokeRole(DEFAULT_ADMIN_ROLE, address(this))` directly, bypassing `proposeAdmin` / `acceptAdmin` entirely. The two-step mechanism intended to prevent accidental handoffs provides no protection because the inherited one-step path remains accessible.

Additionally, the inherited functions allow granting `DEFAULT_ADMIN_ROLE` to multiple addresses simultaneously, which the `admin` state variable (which tracks only one address) would not reflect — creating a split-brain state between actual role holders and the tracked admin.

**Impact:** The two-step transfer safety guarantee is illusory. Admins can accidentally or maliciously transfer the role in a single transaction. The `admin` state variable can diverge from the true `DEFAULT_ADMIN_ROLE` holder(s).

**Recommended Mitigation:** Override `grantRole` and `revokeRole` to revert when called with `DEFAULT_ADMIN_ROLE`, forcing all `DEFAULT_ADMIN_ROLE` transfers through the two-step mechanism:

```solidity
function grantRole(bytes32 role, address account) public override {
    require(role != DEFAULT_ADMIN_ROLE, "use proposeAdmin/acceptAdmin");
    super.grantRole(role, account);
}

function revokeRole(bytes32 role, address account) public override {
    require(role != DEFAULT_ADMIN_ROLE, "use proposeAdmin/acceptAdmin");
    super.revokeRole(role, account);
}
```

**Myriad:** Fixed in commit [`dabc0d7`](https://github.com/Polkamarkets/polkamarkets-js/commit/dabc0d791e0a770f78f160d4ca2537881962d496)

**Cyfrin:** Verified.
