---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-2-4
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2026-01-05T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-05-cyfrin-statusl2-v2-0
title: Griefer can block user from claiming airdrop
vuln_class: []
---

# Griefer can block user from claiming airdrop

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-05-cyfrin-statusl2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md)_

---

**Description:** Function `KarmaAirdrop::claim` claims airdrop and delegates voting power via a call to `Erc20Votes::delegateBySig`:
```solidity
    function claim(
        uint256 index,
        address account,
        uint256 amount,
        bytes32[] calldata merkleProof,
        uint256 nonce,
        uint256 expiry,
        uint8 v,
        bytes32 r,
        bytes32 s
    )
        external
    {
        if (merkleRoot == bytes32(0)) {
            revert KarmaAirdrop__MerkleRootNotSet();
        }
        if (isClaimed(index)) {
            revert KarmaAirdrop__AlreadyClaimed();
        }

        // Verify the merkle proof.
        /// forge-lint: disable-next-line(asm-keccak256)
        bytes32 node = keccak256(abi.encodePacked(index, account, amount));
        if (!MerkleProof.verify(merkleProof, merkleRoot, node)) {
            revert KarmaAirdrop__InvalidProof();
        }

        // Mark it claimed and send the token.
        _setClaimed(index);
        if (!IERC20(TOKEN).transfer(account, amount)) {
            revert KarmaAirdrop__TransferFailed();
        }

        // If the account has no karma balance before this claim, delegate to the default delegatee
        if (IERC20(TOKEN).balanceOf(account) == amount) {
@>          IVotes(TOKEN).delegateBySig(DEFAULT_DELEGATEE, nonce, expiry, v, r, s);
        }
    }
```

There is known vulnerability with EIP2612 permit: signature can be observed in mempool and executed separately, making original call revert. Suppose following example:
1) User sends transaction to mempool, there is no way to not use signature during first claim
2) Griefer observes mempool, notices signature
3) Griefer frontruns by executing `delegateBySig` separately
4) Now claim transaction is executed. Nonce is already used, so signature is invalid and therefore transaction reverts:
```solidity
    function delegateBySig(
        address delegatee,
        uint256 nonce,
        uint256 expiry,
        uint8 v,
        bytes32 r,
        bytes32 s
    ) public virtual {
        if (block.timestamp > expiry) {
            revert VotesExpiredSignature(expiry);
        }
        address signer = ECDSA.recover(
            _hashTypedDataV4(keccak256(abi.encode(DELEGATION_TYPEHASH, delegatee, nonce, expiry))),
            v,
            r,
            s
        );
@>      _useCheckedNonce(signer, nonce);
        _delegate(signer, delegatee);
    }

    function _useCheckedNonce(address owner, uint256 nonce) internal virtual {
        uint256 current = _useNonce(owner);
        if (nonce != current) {
@>          revert InvalidAccountNonce(owner, current);
        }
    }
```

**Impact:** User can be blocked from claiming airdrop.

**Recommended Mitigation:** Wrap call to `Erc20VotesUpgradeable::delegateBySig` into try-catch and in catch ensure there is already sufficient allowance.

**StatusL2:** Fixed in [f9b97ab](https://github.com/status-im/status-network-monorepo/commit/f9b97ab93956cc4d0fbd8ca3687c25a2dceef856).

**Cyfrin:** Verified.
