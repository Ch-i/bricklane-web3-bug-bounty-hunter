---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-1-4
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: Hardcoding deadline for `permit()` will mess up the `structHash` leading to
  an invalid signature
vuln_class: []
---

# Hardcoding deadline for `permit()` will mess up the `structHash` leading to an invalid signature

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** Functions allowing users to grant ERC20 approvals via Permit incorrectly hardcode the deadline passed to permit().
```solidity
function pledge(PledgeData calldata data) external nonReentrant {
        ...

        //5 minute deadline
        if (data.usePermit) {
            IERC20Permit(stablecoin).permit(
                signer,
                address(this),
                finalStablecoinAmount,
//@audit-issue => hardcoded deadline
                block.timestamp + 300,
                data.permitV,
                data.permitR,
                data.permitS
            );
        }
        ...
}
```
The problem is that the recovered signature will be invalid because the deadline is a parameter of the structHash, and, if the signed deadline differs even by 1 second, that hashed structHash will be different than the one that was actually signed by the user.

```solidity
function permit(
        address owner,
        address spender,
        uint256 value,
        uint256 deadline,
        uint8 v,
        bytes32 r,
        bytes32 s
    ) public virtual {
        if (block.timestamp > deadline) {
            revert ERC2612ExpiredSignature(deadline);
        }

//@audit-issue => A hardcoded deadline will mess up the structHash
        bytes32 structHash = keccak256(abi.encode(PERMIT_TYPEHASH, owner, spender, value, _useNonce(owner), deadline));

        bytes32 hash = _hashTypedDataV4(structHash);

//@audit-issue => A different hash than the actual hash signed by the signer will recover a != signer (even address(0)
        address signer = ECDSA.recover(hash, v, r, s);
        if (signer != owner) {
            revert ERC2612InvalidSigner(signer, owner);
        }

        _approve(owner, spender, value);
    }
```

**Impact:** Functions like `pledge()`, `refundToken()` that allows to authorize ERC20Tokens via permit won't work because the structHash will be different than the actual hash signed by the user.

**Recommended Mitigation:** Receive the deadline as a parameter instead of hardcoding it.

```diff
function pledge(PledgeData calldata data) external nonReentrant {
        ...

        //5 minute deadline
        if (data.usePermit) {
            IERC20Permit(stablecoin).permit(
                signer,
                address(this),
                finalStablecoinAmount,
-              block.timestamp + 300,
+              data.deadline,
                data.permitV,
                data.permitR,
                data.permitS
            );
        }
        ...
}
```

**Remora:** Fixed in [5510920](https://github.com/remora-projects/remora-smart-contracts/commit/55109201b0b592abb94a3c73a5f45c9c24b3d440) by removing the permit functionality.

**Cyfrin:** Verified.
