---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-11-05-cyfrin-farcaster-0-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-11-05T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-05-cyfrin-farcaster.md
tags:
- firm:cyfrin
- report:2023-11-05-cyfrin-farcaster
title: A removal signature might be applied to the wrong `fid`.
vuln_class: []
---

# A removal signature might be applied to the wrong `fid`.

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2023-11-05-cyfrin-farcaster.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-05-cyfrin-farcaster.md)_

---

**Severity:** Medium

**Description:** A remove signature is used to remove a key from `fidOwner` using `KeyRegistry.removeFor()`. And the signature is verified in `_verifyRemoveSig()`.

```solidity
    function _verifyRemoveSig(address fidOwner, bytes memory key, uint256 deadline, bytes memory sig) internal {
        _verifySig(
            _hashTypedDataV4(
                keccak256(abi.encode(REMOVE_TYPEHASH, fidOwner, keccak256(key), _useNonce(fidOwner), deadline))
            ),
            fidOwner,
            deadline,
            sig
        );
    }
```

But the signature doesn't specify a `fid` to remove and the below scenario would be possible.

- Alice is an owner of `fid1` and she created a removal signature to remove a `key` but it's not used yet.
- For various reasons, she became an owner of `fid2`.
- `fid2` has a `key` also but she doesn't want to remove it.
- But if anyone calls `removeFor()` with her previous signature, the `key` will be removed from `fid2` unexpectedly.

Once a key is removed, `KeyState` will be changed to `REMOVED` and anyone including the owner can't retrieve it.

**Impact:** A key remove signature might be used for an unexpected `fid`.

**Recommended Mitigation:** The removal signature should contain `fid` also to be invalidated for another `fid`.

**Client:**
Acknowledged. This is an intentional design tradeoff that makes it possible to register a fid and add a key in a single transaction, without knowing the caller's assigned fid in advance. We accept that this has the consequence described in the finding, and users should interpret key registry actions as “add key to currently owned fid.”

Nonces provide some protection against this scenario: if Alice wants to revoke her previous signature intended for `fid1`, she can increment her nonce to invalidate the signature.

**Cyfrin:** Acknowledged.
