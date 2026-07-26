---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-28-cyfrin-rocko-refinance-v2-0-1-6
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-03-28T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-28-cyfrin-rocko-refinance-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-28-cyfrin-rocko-refinance-v2-0
title: Provide a way for users to revoke all approvals
vuln_class: []
---

# Provide a way for users to revoke all approvals

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-28-cyfrin-rocko-refinance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-28-cyfrin-rocko-refinance-v2.0.md)_

---

**Description:** `RockoFlashRefinance` is designed to move existing loan positions from one lending protocol to another. On behalf of the user the contract must be able to:
* close the loan from the previous lending provider
* open a new loan on the new lending provider

For Aave, users must allow the refinance contract to spend the [AToken](https://github.com/aave/aave-v3-core/blob/master/contracts/protocol/tokenization/AToken.sol) to close the position and to spend the [VariableDebtToken](https://github.com/aave/aave-v3-core/blob/master/contracts/protocol/tokenization/VariableDebtToken.sol) to open a new position.

For Compound (Comet), users must allow the refinance contract by calling the [allow function](https://github.com/compound-finance/comet/blob/68cd639c67626c86e890e5aac775ad4b6405d923/contracts/CometExt.sol#L162C14-L162C19).

For Morpho, users must authorize the refinance protocol by calling the [setAuthorization](https://github.com/morpho-org/morpho-blue/blob/9e2b0755b47bbe5b09bf1be8f00e060d4eab6f1c/src/Morpho.sol#L437C14-L437C30) function.

The protocol team provided their frontend source related to these approvals and there were only "approving" support, not revoking. It is recommended to provide an easy way for users to revoke all these approvals.

**Rocko:** Users revokes will be included in the batch transaction when called from the Rocko app.
