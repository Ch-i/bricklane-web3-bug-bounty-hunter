---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-04-28-tokentable-merkle-distributor-0-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-04-28T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-28-TokenTable-Merkle-Distributor.md
tags:
- firm:codespect
- report:2025-04-28-tokentable-merkle-distributor
title: '[M-01] Incorrect Withdrawal Implementation May Lead to Lock of Unclaimed NFTs'
vuln_class: []
---

# [M-01] Incorrect Withdrawal Implementation May Lead to Lock of Unclaimed NFTs

_Section severity (from Solodit section header): Medium_  
_Audit firm: CODESPECT_  
_Source report: [2025-04-28-TokenTable-Merkle-Distributor.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-28-TokenTable-Merkle-Distributor.md)_

---

**Files:** [SimpleERC721MerkleDistributor.sol](https://github.com/EthSign/merkle-token-distributor/tree/96fedd0d945693149e0903c84502004bf819996c/src/core/extensions/SimpleERC721MerkleDistributor.sol#L12)

**Description:**

The `SimpleERC721MerkleDistributor` contract allows claiming of ERC721 tokens instead of ERC20. It inherits most of its functions from `TokenTableMerkleDistributor`. The main difference is that `_send()` and `withdraw()` functions handle ERC721 token minting and transfers instead of ERC20 transfers.

The claiming process in this case relies on minting the NFTs directly from the token contract. In the ERC20 versions the project owner is equipped with `withdraw()`, which allows to recover all non-claimed tokens.

In this `SimpleERC721MerkleDistributor` contract, however the the overloaded `withdraw()` attempts to transfer existing NFTs from the contract. This will not work because the unclaimed NFTs are not actually minted to that contract.

```solidity
function withdraw(bytes memory extraData) external virtual override onlyOwner {
    uint256[] memory tokenIds = abi.decode(extraData, (uint256[]));
    for (uint256 i = 0; i < tokenIds.length; i++) {
        IERC721(_getBaseMerkleDistributorStorage().token).safeTransferFrom(address(this), owner(), tokenIds[i]);
    }
}

function _send(address recipient, address token, uint256 amount) internal virtual override {
    for (uint256 i = 0; i < amount; i++) {
        IERC721SafeMintable(token).safeMint(recipient);
    }
}
```

**Impact:** In the case where the minting permissions are granted to the distributor contract, but not to the project owner, the owner cannot mint the unclaimed tokens for himself and they might end up locked (or rather never minted).

**Recommendation(s):** Change the `withdraw()` function in `SimpleERC721MerkleDistributor` so that it mints the NFTs instead of transferring them. Warning! If that change is implemented the `withdraw()` function must also be placed into the `SimpleNoMintERC721MerkleDistributor` contract as it inherits from `SimpleERC721MerkleDistributor`. If that is not done, then withdrawals will not work for `SimpleNoMintERC721MerkleDistributor`.

**Status:** Fixed

**Update from TokenTable:** Revised withdraw logic in `0e4cd1d1c27dfbb98080728da8955a10d1143a9c`.
