---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-15-cyfrin-veefriends-v2-0-0-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-10-15T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-15-cyfrin-veefriends-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-15-cyfrin-veefriends-v2-0
title: Inconsistent state updates when tokens are burned and/or transferred directly
  to the `DEAD_ADDRESS`
vuln_class: []
---

# Inconsistent state updates when tokens are burned and/or transferred directly to the `DEAD_ADDRESS`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-15-cyfrin-veefriends-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-15-cyfrin-veefriends-v2.0.md)_

---

**Description:** The following state updates are performed when batch burning tokens:

```solidity
    function _burnBatch(uint256[] calldata tokenIds) internal virtual {
        for (uint256 i; i < tokenIds.length; i++) {
            uint256 tokenId = tokenIds[i];
            address owner = ownerOf(tokenId);

            _beforeTokenTransfer(owner, DEAD_ADDRESS, tokenId, 1);

            // Clear approvals
@>          delete _tokenApprovals[tokenId];

            unchecked {
                // Cannot overflow, as that would require more tokens to be burned/transferred
                // out than the owner initially received through minting and transferring in.
@>              _balances[owner] -= 1;
            }

@>          _owners[tokenId] = DEAD_ADDRESS;

            emit Transfer(owner, DEAD_ADDRESS, tokenId);

            _afterTokenTransfer(owner, DEAD_ADDRESS, tokenId, 1);
        }

        unchecked {
@>          _burnCounter += tokenIds.length;
        }
    }
```

Note how while the `_balances[owner]` state is decremented, that of `DEAD_ADDRESS` is not incremented despite being granted ownership.

Now consider the direct transfer of a token to the `DEAD_ADDRESS`. While this is likely not desirable, there exists an asymmetry in that the balance this time will be updated while the `_burnCounter` state remains unchanged:

```solidity
    function _transfer(
        address from,
        address to,
        uint256 tokenId
    ) internal virtual {
        if (to == address(0)) {
            revert ERC721VFTransferToTheZeroAddress();
        }

        if (ownerOf(tokenId) != from) {
            revert ERC721VFTransferFromIncorrectOwner(from, tokenId);
        }

        _beforeTokenTransfer(from, to, tokenId, 1);

        // Clear approvals from the previous owner
        delete _tokenApprovals[tokenId];

        unchecked {
            // `_balances[from]` cannot overflow for the same reason as described in `_burn`:
            // `from`'s balance is the number of token held, which is at least one before the current
            // transfer.
            // `_balances[to]` could overflow in the conditions described in `_mint`. That would require
            // all 2**256 token ids to be minted, which in practice is impossible.
            _balances[from] -= 1;
@>          _balances[to] += 1;
        }
@>      _owners[tokenId] = to;

        emit Transfer(from, to, tokenId);

        _afterTokenTransfer(from, to, tokenId, 1);
    }
```

**Impact:** State is partially corrupted when burning and/or transferring tokens directly to `DEAD_ADDRESS`.

**Recommended Mitigation:** Increment `_balances[DEAD_ADDRESS]` when tokens are burned. Additionally consider restricting direct token transfers to the `DEAD_ADDRESS`, or at least ensure this edge case is handled to remain consistent with the expected burn mechanics.

**VeeFriends:** Fixed in commits [dc834fa](https://github.com/veefriends/smart-contracts-v2/commit/dc834fad574e9f7caf460ba5eae2983f8d0e4488) and [ed976c6](https://github.com/veefriends/smart-contracts-v2/commit/ed976c671033b145b9055337218196dfb2e642ae).

**Cyfrin:** Verified. The dead address balance is now incremented on burning and direct transfers are no longer permitted.

\clearpage
