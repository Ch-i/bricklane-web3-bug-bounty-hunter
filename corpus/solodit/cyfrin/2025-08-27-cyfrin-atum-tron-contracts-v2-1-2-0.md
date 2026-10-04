---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-27-cyfrin-atum-tron-contracts-v2-1-2-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-08-27T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-27-cyfrin-atum-tron-contracts-v2.1.md
tags:
- firm:cyfrin
- report:2025-08-27-cyfrin-atum-tron-contracts-v2-1
title: Use TRON `isContract` to determine whether an address is a contract
vuln_class: []
---

# Use TRON `isContract` to determine whether an address is a contract

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-27-cyfrin-atum-tron-contracts-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-27-cyfrin-atum-tron-contracts-v2.1.md)_

---

**Description:** TRON has a special opcode `ISCONTRACT` added in [TIP-44](https://github.com/tronprotocol/tips/blob/master/tip-44.md) for determining whether an address is a contract or not.

Use this in the permit2 fork at https://github.com/alexroan/permit2-tron/blob/main/contracts/libraries/SignatureVerification.sol#L26 doing something like:
```diff
-       if (claimedSigner.code.length == 0) {
+       if (!claimedSigner.isContract) {
```

However the existing code appears to function correctly as well so there is no significant reason to change this. `SignatureChecker::isValidSignatureNow` used by the `Escrow` contract also uses the [same code length](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/cryptography/SignatureChecker.sol#L33).

**Atum:**
Acknowledged.
