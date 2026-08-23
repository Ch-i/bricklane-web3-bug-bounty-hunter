---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2-2-2-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-08-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md
tags:
- firm:cyfrin
- report:2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2-2
title: Incorrect function documentation
vuln_class: []
---

# Incorrect function documentation

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md)_

---

**Description:** The `SegregatedVault::addAggregator` function contains incorrect documentation that mentions "Operators" instead of "Aggregators" in both the function description and parameter documentation. The comment states "Operators can deposit and redeem. Emits AggregatorAdded event" when it should describe aggregator capabilities, and the parameter description says "The address to which the Operator role will be granted" when it should reference the Aggregator role.

This appears to be a copy-paste error from the `addOperator` function documentation. The same issue exists in `SecuritizeVaultV2::addAggregator`.

Additionally, there is another inconsistency in `SegregatedVault::revokeAggregator` where the comment states "Revokes the Operator role from an account. Emits a OperatorRevoked event" when it should reference the Aggregator role and AggregatorRevoked event.

**Impact:** Incorrect documentation may confuse developers and auditors about the intended role permissions and capabilities, potentially leading to integration errors or security misunderstandings.

**Recommended Mitigation:** Update the documentation to correctly describe aggregator role capabilities and parameters:

```diff
/**
 * @dev Grants the aggregator role to an account.
- * Operators can deposit and redeem. Emits AggregatorAdded event
+ * Aggregators can manage vault operations and perform deposits/redeems on behalf of the protocol. Emits AggregatorAdded event
 *
- * @param account The address to which the Operator role will be granted.
+ * @param account The address to which the Aggregator role will be granted.
 */
function addAggregator(address account) external addressNotZero(account) onlyRole(DEFAULT_ADMIN_ROLE) {
    _grantRole(AGGREGATOR_ROLE, account);
    emit AggregatorAdded(account);
}
```

Apply similar fixes to `SegregatedVault::revokeAggregator` and `SecuritizeVaultV2::addAggregator` functions.

**Securitize:** Fixed in commits [0e881e](https://github.com/securitize-io/bc-securitize-vault-sc/commit/0e881e38f9ec600d7ee5b1b7555a4ab81eaa04d1) and [402daa](https://github.com/securitize-io/bc-rwa-seg-wrap-sc/commit/402daa31d16471b24ea42810d613064b38256a00).

**Cyfrin:** Verified.
