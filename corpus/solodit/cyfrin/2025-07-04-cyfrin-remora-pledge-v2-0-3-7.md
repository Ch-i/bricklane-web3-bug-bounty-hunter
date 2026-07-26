---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-3-7
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: Use `EIP712Upgradeable` library to simplify `DocumentManager`
vuln_class: []
---

# Use `EIP712Upgradeable` library to simplify `DocumentManager`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** Use [`EIP712Upgradeable`](https://github.com/OpenZeppelin/openzeppelin-contracts-upgradeable/blob/master/contracts/utils/cryptography/EIP712Upgradeable.sol) library to simplify `DocumentManager` as this library provides the domain separator and the helpful function `_hashTypedDataV4`.

Inherit from `EIP712Upgradeable`, remove all the duplicate code which it provides then in `verifySignature` do this:
```diff
-        bytes32 digest = keccak256(
-            abi.encodePacked("\x19\x01", _DOMAIN_SEPARATOR, structHash)
-        );
+        bytes32 digest = _hashTypedDataV4(structHash);
```

**Remora:** Fixed in commit [b545498](https://github.com/remora-projects/remora-smart-contracts/commit/b545498ed931eb63ae0ec7f6fb3297ce25886281).

**Cyfrin:** Verified.
