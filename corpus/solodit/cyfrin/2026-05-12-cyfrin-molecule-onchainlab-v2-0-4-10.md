---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-12-cyfrin-molecule-onchainlab-v2-0-4-10
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-05-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-12-cyfrin-molecule-onchainlab-v2-0
title: '`OnChainLab::owner` returns `address(0)` when not on the canonical chain,
  silent fallback'
vuln_class: []
---

# `OnChainLab::owner` returns `address(0)` when not on the canonical chain, silent fallback

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-12-cyfrin-molecule-onchainlab-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md)_

---

**Description:** `OnChainLab::owner` returns `address(0)` if `chainId != CANONICAL_CHAIN_ID` (Base mainnet, 8453). This value flows into `signer`, which is used by `_isValidSigner`, `onlyEntryPointOrOwner`, ERC-1271 verification, and EIP-7739 signature validation. A non-canonical-chain caller observes `signer() == address(0)`, which is the sentinel "no signer." Any check `recovered == owner()` that succeeds with `recovered == address(0)` would falsely authorize. While in practice ECDSA recovery cannot return `address(0)` for a valid signature (and Solady ECDSA reverts on invalid recovery), the silent fallback removes the only chain-binding check from a critical surface - an upgrade or refactor that introduces a different signer source could land on this `address(0)` ambient value.

```solidity
src/OnChainLab.sol
618:    function owner() public view virtual returns (address) {
619:        (uint256 chainId, address tokenContract, uint256 tokenId) = token();
620:        if (chainId != CANONICAL_CHAIN_ID) return address(0);
621:
622:        return IERC721(tokenContract).ownerOf(tokenId);
623:    }
```

**Recommended Mitigation:** Revert with a typed error on chain mismatch instead of returning `address(0)`:

```solidity
error WrongChain(uint256 actual, uint256 expected);

function owner() public view virtual returns (address) {
    (uint256 chainId, address tokenContract, uint256 tokenId) = token();
    if (chainId != CANONICAL_CHAIN_ID) revert WrongChain(chainId, CANONICAL_CHAIN_ID);
    return IERC721(tokenContract).ownerOf(tokenId);
}
```

This makes cross-chain misuse loud rather than silent and removes the `address(0)` poison value from downstream signature checks.

**Molecule:** Fixed in commit [042de94](https://github.com/moleculeprotocol/onchainlabs/commit/042de94).

**Cyfrin:** Verified.
