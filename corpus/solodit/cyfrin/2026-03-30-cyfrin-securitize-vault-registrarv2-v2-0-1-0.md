---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-30-cyfrin-securitize-vault-registrarv2-v2-0-1-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-03-30T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-30-cyfrin-securitize-vault-registrarv2-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-30-cyfrin-securitize-vault-registrarv2-v2-0
title: Investor Cannot Revoke Standing Permission for a Removed Operator
vuln_class: []
---

# Investor Cannot Revoke Standing Permission for a Removed Operator

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-30-cyfrin-securitize-vault-registrarv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-30-cyfrin-securitize-vault-registrarv2-v2.0.md)_

---

**Description:** `VaultRegistrar::invalidateOperatorPermission` guards the revocation call with a check that requires the target `operator` to currently hold `OPERATOR_ROLE`:

```solidity
// VaultRegistrar.sol:162
function invalidateOperatorPermission(address operator) external notZeroAddress(operator) {
    if (!hasRole(OPERATOR_ROLE, operator)) revert NotAnOperator(operator);   // ← blocks revocation
    uint256 newNonce = ++_operatorNonces[_msgSender()][operator];
    emit OperatorPermissionInvalidated(_msgSender(), operator, newNonce);
}
```

When admin calls `removeOperator(operatorA)`, the operator loses `OPERATOR_ROLE`. Any investor who previously signed a long-lived standing permission for that operator can no longer increment their per-operator nonce, because the call reverts with `NotAnOperator`.

**Impact:** An investor's standing permission for a removed operator is permanently unrevocable until the deadline passes. If `OPERATOR_ROLE` is later re-granted to the same address (routine re-onboarding, key rotation, admin key compromise), the old, investor-unrevocable signature becomes immediately usable again — allowing the re-granted operator to register arbitrary vaults under the investor's identity within the original deadline window.

The code comment justifies the check as: *"a non-operator cannot call registerVault regardless, so revoking them has no effect."* This reasoning breaks down when the operator's role is restored: the old signature becomes valid again, and the investor has lost the ability to pre-emptively revoke consent during the intervening period.

**Proof of Concept:**
1. Admin grants `OPERATOR_ROLE` to `operatorA`
2. Alice signs a 90-day standing permission for `operatorA`
3. Day 10: `operatorA` is compromised; admin calls `removeOperator(operatorA)`
4. Day 10: Alice calls `invalidateOperatorPermission(operatorA)` → **reverts** with `NotAnOperator`
5. Day 20: Admin re-grants `OPERATOR_ROLE` to `operatorA` (after believing the situation is resolved)
6. Day 20–90: `operatorA` uses Alice's original signature to register vaults under her identity


**Recommended Mitigation:** Remove the `hasRole` check from `invalidateOperatorPermission`. An investor should always be able to increment their own nonce for any address, regardless of whether the operator holds a role:

```solidity
function invalidateOperatorPermission(address operator) external notZeroAddress(operator) {
    uint256 newNonce = ++_operatorNonces[_msgSender()][operator];
    emit OperatorPermissionInvalidated(_msgSender(), operator, newNonce);
}
```

**Securitize:** Fixed in commit [58a5856](https://github.com/securitize-io/bc-vault-registrar/commit/58a585655478b80752a58a4e2c0b2f510409aed0)

**Cyfrin:** Verified. Investor can now revoke standing permission for a removed Operator
