---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-04-cyfrin-securitize-compliance-permissionless-diff-v2-0-1-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-06-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-04-cyfrin-securitize-compliance-permissionless-diff-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-04-cyfrin-securitize-compliance-permissionless-diff-v2-0
title: '`ComplianceServicePermissionless::preIssuanceCheck` omits the pause check,
  allowing issuance while the token is paused contrary to FR-4'
vuln_class: []
---

# `ComplianceServicePermissionless::preIssuanceCheck` omits the pause check, allowing issuance while the token is paused contrary to FR-4

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-04-cyfrin-securitize-compliance-permissionless-diff-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-04-cyfrin-securitize-compliance-permissionless-diff-v2.0.md)_

---

**Description:** The audit-scope document FR-4 states: *"All transfers and issuances must be rejected with code 10 while paused. Burn and seize are exempt from the pause check."*

Transfers honor this. Issuance does not — the pause flag is never read on the issuance path.

The new permissionless `preIssuanceCheck` checks only zero-address and blacklist:

```solidity
// compliance/ComplianceServicePermissionless.sol
function preIssuanceCheck(address _to, uint256 /*_value*/)
    public view virtual override returns (uint256 code, string memory reason)
{
    if (_to == address(0)) {
        return (101, "Zero address");
    }
    if (getBlackListManager().isBlacklisted(_to)) {
        return (100, WALLET_BLACKLISTED); // @audit no code-10 pause branch — FR-4 requires rejecting issuance while paused
    }
    return (0, VALID);
}
```

The enforcing function `ComplianceService:validateIssuance` likewise never reads the pause flag:

```solidity
// compliance/ComplianceService.sol
function validateIssuance(address _to, uint256 _value, uint256 _issuanceTime) public override onlyToken returns (bool) {
    ...
    require(authorizedSecurities == 0 || totalSupply + _value <= authorizedSecurities, MAX_AUTHORIZED_SECURITIES_EXCEEDED);
    (code, reason) = preIssuanceCheck(_to, _value); // @audit no pause check inside; no whenNotPaused on caller
    require(code == 0, reason);
    uint256 issuanceTime = validateIssuanceTime(_issuanceTime);
    return recordIssuance(_to, _value, issuanceTime);
}
```

Contrast with the transfer path, which DOES honor the pause: `DSToken:canTransfer` passes `paused` into `validateTransfer`, and `ComplianceServicePermissionless:newPreTransferCheck` returns `(10, TOKEN_PAUSED)` as its first check:

```solidity
// compliance/ComplianceServicePermissionless.sol — newPreTransferCheck
if (_pausedToken) {
    return (10, TOKEN_PAUSED); // @audit transfers correctly reject while paused — issuance has no equivalent
}
```

**Impact:** An Issuer (or Master) can mint new tokens while the token is paused, contrary to FR-4. Pausing is an emergency control; allowing minting during that window weakens the "everything is frozen" guarantee operators expect, and permits supply inflation (holder dilution) during a freeze.

**Recommended Mitigation:** If FR-4 is the intended behavior, consider adding a pause branch to the permissionless `preIssuanceCheck`.


**Securitize:** Acknowledged. Working as designed, the spec document (FR-4) will be updated.
