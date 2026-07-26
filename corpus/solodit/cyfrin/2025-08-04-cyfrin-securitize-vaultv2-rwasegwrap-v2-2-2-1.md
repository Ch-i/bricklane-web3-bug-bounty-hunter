---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2-2-2-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-08-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md
tags:
- firm:cyfrin
- report:2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2-2
title: Single-step admin transfer creates risk of permanent loss of administrative
  control
vuln_class: []
---

# Single-step admin transfer creates risk of permanent loss of administrative control

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md)_

---

**Description:** The `SegregatedVault::changeAdmin` function implements a single-step admin transfer mechanism that immediately grants admin privileges to the new address and revokes them from the current admin in a single transaction. This pattern creates a risk where administrative control can be permanently lost if an incorrect address is provided, as there is no validation that the new admin can actually control the contract.

The same unsafe single-step admin transfer pattern is implemented across multiple contracts in the codebase:
- `VaultDeployer::changeAdmin` performs immediate admin role transfer
- `SecuritizeVaultV2::changeAdmin` uses the same single-step approach
- `SecuritizeVault::changeAdmin` also implements immediate transfer

The admin role has extensive privileges including the ability to add/revoke operators, liquidators, and aggregators, as well as control over vault upgrades and configuration. Losing admin access would render these administrative functions permanently inaccessible, potentially freezing protocol operations and preventing emergency responses.

**Impact:** A typographical error or incorrect address during admin transfer would result in permanent loss of administrative control over the contract, rendering critical management functions inaccessible and potentially requiring expensive redeployment procedures.

**Recommended Mitigation:** Implement a two-step admin transfer pattern where the new admin must explicitly accept the role:

```diff
+ address public pendingAdmin;

+ function transferAdmin(address newAdmin) external addressNotZero(newAdmin) onlyRole(DEFAULT_ADMIN_ROLE) {
+     pendingAdmin = newAdmin;
+     emit AdminTransferStarted(msg.sender, newAdmin);
+ }

+ function acceptAdmin() external {
+     if (msg.sender != pendingAdmin) {
+         revert NotPendingAdmin();
+     }
+     address oldAdmin = msg.sender;
+     _grantRole(DEFAULT_ADMIN_ROLE, pendingAdmin);
+     _revokeRole(DEFAULT_ADMIN_ROLE, oldAdmin);
+     delete pendingAdmin;
+     emit AdminChanged(pendingAdmin);
+ }

- function changeAdmin(address newAdmin) external addressNotZero(newAdmin) onlyRole(DEFAULT_ADMIN_ROLE) {
-     _grantRole(DEFAULT_ADMIN_ROLE, newAdmin);
-     _revokeRole(DEFAULT_ADMIN_ROLE, msg.sender);
-     emit AdminChanged(newAdmin);
- }
```

Apply similar changes to `VaultDeployer`, `SecuritizeVaultV2`, and `SecuritizeVault` contracts.

**Securitize:** Acknowledged.

**Cyfrin:** Acknowledged.
