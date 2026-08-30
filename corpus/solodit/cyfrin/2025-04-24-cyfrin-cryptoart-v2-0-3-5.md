---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-cryptoart-v2-0-3-5
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-04-24T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-cryptoart-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-24-cyfrin-cryptoart-v2-0
title: To prevent duplicate ids in `_batchBurn`, enforce ascending order instead of
  nested `for` loops
vuln_class: []
---

# To prevent duplicate ids in `_batchBurn`, enforce ascending order instead of nested `for` loops

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-cryptoart-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-cryptoart-v2.0.md)_

---

**Description:** In `_batchBurn` to prevent duplicate ids, instead of using nested `for` loops it is more efficient to [enforce ascending order of ids](https://x.com/DevDacian/status/1734885772829045205) using only 1 `for` loop.

Additionally, the duplicate id check can be completely removed since if there is a duplicate id the second `burn` call will revert. For example this test added to `test/unit/BurnOperationsTest.t.sol`:
```solidity
    function test_DoubleBurn() public {
        // Mint a token to user1
        mintNFT(user1, TOKEN_ID, TOKEN_PRICE, TOKEN_PRICE);
        testAssertions.assertTokenOwnership(nft, TOKEN_ID, user1);

        // First burn should succeed
        vm.prank(user1);
        nft.burn(TOKEN_ID);

        // Second burn should revert since token no longer exists
        vm.prank(user1);
        // vm.expectRevert();
        nft.burn(TOKEN_ID);
    }
```

Results in:
```solidity
    ├─ [4294] TransparentUpgradeableProxy::fallback(1)
    │   ├─ [3940] CryptoartNFT::burn(1) [delegatecall]
    │   │   └─ ← [Revert] ERC721NonexistentToken(1)
    │   └─ ← [Revert] ERC721NonexistentToken(1)
    └─ ← [Revert] ERC721NonexistentToken(1)
```

**CryptoArt:**
Fixed in commit [3c39fb8](https://github.com/cryptoartcom/cryptoart-smart-contracts/commit/3c39fb86db6b92424a0cf55c315d0d6284c267bf).

**Cyfrin:** Verified.

\clearpage
