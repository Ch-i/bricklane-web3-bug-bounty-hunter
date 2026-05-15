---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-27-cyfrin-linea-mixed-upgrade-v2-0-2-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2026-03-27T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-27-cyfrin-linea-mixed-upgrade-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-27-cyfrin-linea-mixed-upgrade-v2-0
title: Inconsistent handling of update/set transactions which don't actually change
  values
vuln_class: []
---

# Inconsistent handling of update/set transactions which don't actually change values

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-27-cyfrin-linea-mixed-upgrade-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-27-cyfrin-linea-mixed-upgrade-v2.0.md)_

---

**Description:** `PauseManager::updatePauseTypeRole` reverts if the previous and new roles are identical, and only writes to storage and emits an event if the value was actually changed:
```solidity
function updatePauseTypeRole(
  PauseType _pauseType,
  bytes32 _newRole
) external onlyUsedPausedTypes(_pauseType) onlyRole(SECURITY_COUNCIL_ROLE) {
  bytes32 previousRole = _pauseTypeRoles[_pauseType];
  if (previousRole == _newRole) {
    revert RolesNotDifferent();
  }

  _pauseTypeRoles[_pauseType] = _newRole;
  emit PauseTypeRoleUpdated(_pauseType, _newRole, previousRole);
}
```

In contrast the following places don't revert on "no change" transactions, writing to storage and emitting events even if no change occurred:

* `LineaRollupBase::setVerifierAddress`
```solidity
function setVerifierAddress(address _newVerifierAddress, uint256 _proofType) external onlyRole(VERIFIER_SETTER_ROLE) {
    if (_newVerifierAddress == address(0)) {
      revert ZeroAddressNotAllowed();
    }
    // no revert if _newVerifierAddress == verifiers[_proofType]
    emit VerifierAddressChanged(_newVerifierAddress, _proofType, msg.sender, verifiers[_proofType]);
    verifiers[_proofType] = _newVerifierAddress;
}
```

* `LineaRollupBase::unsetVerifierAddress`
```solidity
function unsetVerifierAddress(uint256 _proofType) external onlyRole(VERIFIER_UNSETTER_ROLE) {
    // no revert if verifiers[_proofType] == address(0)
    emit VerifierAddressChanged(address(0), _proofType, msg.sender, verifiers[_proofType]);
    delete verifiers[_proofType];
}
```

* `L2MessageServiceV1::setMinimumFee`
```solidity
function setMinimumFee(uint256 _feeInWei) external onlyRole(MINIMUM_FEE_SETTER_ROLE) {
    // no revert if _feeInWei == previousMinimumFee
    uint256 previousMinimumFee = minimumFeeInWei;
    minimumFeeInWei = _feeInWei;
    emit MinimumFeeChanged(previousMinimumFee, _feeInWei, msg.sender);
}
```

* `TokenBridgeBase::setMessageService`
```solidity
function setMessageService(address _messageService) external ... {
    // no revert if _messageService == oldMessageService
    address oldMessageService = address(messageService);
    messageService = IMessageService(_messageService);
    emit MessageServiceUpdated(_messageService, oldMessageService, msg.sender);
}
```

* `RateLimiter::resetAmountUsedInPeriod`
```solidity
function resetAmountUsedInPeriod() external onlyRole(USED_RATE_LIMIT_RESETTER_ROLE) {
    // no revert if currentPeriodAmountInWei == 0
    currentPeriodAmountInWei = 0;
    emit AmountUsedInPeriodReset(_msgSender());
}
```

**Recommended Mitigation:** This can be acknowledged or behavior can be harmonized if there is no specific reasons for one function to differ in behavior from others.

**Linea:** Acknowledged.
