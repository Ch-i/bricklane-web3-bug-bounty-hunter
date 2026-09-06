---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-27-cyfrin-linea-mixed-upgrade-v2-0-2-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-03-27T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-27-cyfrin-linea-mixed-upgrade-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-27-cyfrin-linea-mixed-upgrade-v2-0
title: '`LineaRollup, LivenessRecovery::renounceRole` prevents liveness recovery operator
  from renouncing all roles'
vuln_class: []
---

# `LineaRollup, LivenessRecovery::renounceRole` prevents liveness recovery operator from renouncing all roles

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-27-cyfrin-linea-mixed-upgrade-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-27-cyfrin-linea-mixed-upgrade-v2.0.md)_

---

**Description:** The intention appears to be that the liveness recovery operator shouldn't be able to renounce the `OPERATOR_ROLE` they are granted, however `LivenessRecovery::renounceRole` called by `LineaRollup::renounceRole` prevents the liveness recovery operator from renouncing *all* roles:
```solidity
function renounceRole(bytes32 _role, address _account) public virtual override {
  // @audit only checks address, not role being renounced
  if (_account == livenessRecoveryOperator) {
    revert OnlyNonLivenessRecoveryOperator();
  }

  super.renounceRole(_role, _account);
}
```

**Impact:** If the liveness recovery operator has other legitimate roles they wish to renounce, they will be unable to do so.

**Recommended Mitigation:** `LivenessRecovery::renounceRole` should only revert if `OPERATOR_ROLE` is being renounced:
```diff
function renounceRole(bytes32 _role, address _account) public virtual override {
- if (_account == livenessRecoveryOperator) {
+ if (_account == livenessRecoveryOperator && _role == OPERATOR_ROLE) {
    revert OnlyNonLivenessRecoveryOperator();
  }
  super.renounceRole(_role, _account);
}
```

**Linea:** Acknowledged; the liveness operator role should never and would never be granted anything other than the operator role.
