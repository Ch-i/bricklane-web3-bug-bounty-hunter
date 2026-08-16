---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-27-cyfrin-linea-mixed-upgrade-v2-0-2-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-03-27T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-27-cyfrin-linea-mixed-upgrade-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-27-cyfrin-linea-mixed-upgrade-v2-0
title: '`LivenessRecovery::setLivenessRecoveryOperator` will emit misleading event
  when role is not granted'
vuln_class: []
---

# `LivenessRecovery::setLivenessRecoveryOperator` will emit misleading event when role is not granted

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-27-cyfrin-linea-mixed-upgrade-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-27-cyfrin-linea-mixed-upgrade-v2.0.md)_

---

**Description:** `LivenessRecovery::setLivenessRecoveryOperator` can be called multiple times as long as the first two preconditions are met.

However if `OPERATOR_ROLE` has already been granted to `livenessRecoveryOperator` then `AccessControlUpgradeable::_grantRole` [returns](https://github.com/OpenZeppelin/openzeppelin-contracts-upgradeable/blob/master/contracts/access/AccessControlUpgradeable.sol#L205-L211) `false`.

But the boolean return value of `_grantRole` is not checked so the misleading event will still be emitted.

**Recommended Mitigation:** Only emit the event if `_grantRole` returned true:
```diff
-   _grantRole(OPERATOR_ROLE, livenessRecoveryOperatorAddress);
+   if(_grantRole(OPERATOR_ROLE, livenessRecoveryOperatorAddress))
    emit LivenessRecoveryOperatorRoleGranted(msg.sender, livenessRecoveryOperatorAddress);
```

**Linea:** Fixed in commit [66050d2](https://github.com/Consensys/linea-monorepo/pull/2007/commits/66050d2689a6b817b29f2de6b0a3fda2c69c42d9).

**Cyfrin:** Verified.
