---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-3-6
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: Use `SignatureChecker` library and optionally support `EIP7702` accounts which
  use their private key to sign
vuln_class: []
---

# Use `SignatureChecker` library and optionally support `EIP7702` accounts which use their private key to sign

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** In `DocumentManager::verifySignature` use the [SignatureChecker](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/cryptography/SignatureChecker.sol) library:
```diff
-        if (signer.code.length == 0) {
-            //signer is EOA
-            (address returnedSigner, , ) = ECDSA.tryRecover(digest, signature);
-            result = returnedSigner == signer;
-        } else {
-            //signer is SCA
-            (bool success, bytes memory ret) = signer.staticcall(
-                abi.encodeWithSelector(
-                    bytes4(keccak256("isValidSignature(bytes32,bytes)")),
-                    digest,
-                    signature
-                )
-            );
-            result = (success && ret.length == 32 && bytes4(ret) == MAGICVALUE);
-        }

-        if (!result) revert InvalidSignature();
+        if(!SignatureChecker.isValidSignatureNow(signer, digest, signature)) revert InvalidSignature();
```

Additionally with [EIP7702](https://eip7702.io/), it is now possible for addresses to have `code.length > 0` but still use their private keys to sign; so with the current code or the above recommendation this scenario won't be supported.

To support this scenario check out [this finding](https://solodit.remora-projects.io/issues/verifysignature-is-not-compatible-with-smart-contract-wallets-or-other-smart-accounts-remora-projects-none-evo-soulboundtoken-markdown) from our recent audit where this scenario is also supported by first calling [ECDSA.tryRecover](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/cryptography/ECDSA.sol#L56) then if that didn't work calling `SignatureChecker::isValidERC1271SignatureNow` as the backup option:
```diff
+        (address recovered, ECDSA.RecoverError error,) = ECDSA.tryRecover(digest, signature);
​
+        if (error == ECDSA.RecoverError.NoError && recovered == signer) result = true;
+        else result = SignatureChecker.isValidERC1271SignatureNow(signer, digest, signature);

+        if (!result) revert InvalidSignature();
```

**Remora:** Fixed in commit [b545498](https://github.com/remora-projects/remora-smart-contracts/commit/b545498ed931eb63ae0ec7f6fb3297ce25886281).

**Cyfrin:** Verified.
