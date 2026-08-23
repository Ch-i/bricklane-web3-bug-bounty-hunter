---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-17-cyfrin-stbl-ess-v2-0-2-3
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-06-17T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-17-cyfrin-stbl-ess-v2-0
title: vault upgrade authority is delegated to a mutable wrapper, letting `WRAPPER_MANAGER_ROLE`
  escalate to vault upgrades
vuln_class: []
---

# vault upgrade authority is delegated to a mutable wrapper, letting `WRAPPER_MANAGER_ROLE` escalate to vault upgrades

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-17-cyfrin-stbl-ess-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md)_

---

**Description:** `STBL_XLayer_NFT_Vault::_authorizeUpgrade` checks no role on the vault itself. It forwards the decision to the wrapper:

```solidity
function _authorizeUpgrade(address newImplementation) internal override {
    if (fetchSTBL_ESS_Wrapper() == address(0))
        revert STBL_ESS_InvalidAddress(fetchSTBL_ESS_Wrapper());
    if (
        !iSTBL_XLayer_Wrapper(fetchSTBL_ESS_Wrapper()).hasRole(UPGRADER_ROLE, _msgSender())
    ) revert STBL_UnauthorizedCaller();
    ...
}
```

`UPGRADER_ROLE` is never granted on the vault (`initialize` grants only `DEFAULT_ADMIN_ROLE` and `WRAPPER_MANAGER_ROLE`), so the wrapper's role table is the sole gate. That wrapper pointer is freely repointable by a weaker role:

```solidity
function setWrapper(address _wrapper) external onlyRole(WRAPPER_MANAGER_ROLE) {
    address oldWrapper = fetchSTBL_ESS_Wrapper();
    _Vault_setWrapper(_wrapper);
    emit WrapperUpdated(oldWrapper, _wrapper);
}
```

`_Vault_setWrapper` validates only `_wrapper != address(0)`. A `WRAPPER_MANAGER_ROLE` holder can therefore point the vault at a malicious wrapper whose `hasRole` always returns `true`, then pass any `_authorizeUpgrade` check.

**Impact:** `WRAPPER_MANAGER_ROLE`, an operational role for setting the wrapper pointer and claiming yield, gains the power to upgrade the vault to arbitrary code: drain every custodied YLD NFT and asset token. This is privilege escalation from a weak role to total vault compromise. High.


**Recommended Mitigation:**
1. Check `UPGRADER_ROLE` against a non-mutable authority (the vault's own `AccessControl` table or a fixed registry address) rather than the settable wrapper pointer.
2. Restrict `setWrapper` to `DEFAULT_ADMIN_ROLE` and/or validate the new wrapper against `STBL_Register`.

**STBL:** Fixed in commit [a019128](https://github.com/USD-Pi-Protocol/stbl-contracts-evm-ess-common/commit/a019128b983f40bedec7f4cfb34e3eecadad5c6d).

**Cyfrin:** Verified. `_authorizeUpgrade` on the vault now checks `UPGRADER_ROLE` directly against the vault's own `AccessControl` table instead of delegating to the wrapper.
