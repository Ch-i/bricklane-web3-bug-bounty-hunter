---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-12-cyfrin-molecule-onchainlab-v2-0-3-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-05-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-12-cyfrin-molecule-onchainlab-v2-0
title: '`OnChainLab::owner` chain-id replay guard is dead code'
vuln_class: []
---

# `OnChainLab::owner` chain-id replay guard is dead code

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-12-cyfrin-molecule-onchainlab-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md)_

---

**Description:** The `OnChainLab::owner` function reads a `chainId` value from the bytecode footer (set at account-creation time by the ERC-6551 registry) and compares it against the constant `CANONICAL_CHAIN_ID = 8453`. The factory always passes `config.CANONICAL_CHAIN_ID()` (a constant) as the `chainId` argument to `ERC6551Registry::createAccount` at line 220. The `chainId` returned from the bytecode footer is therefore always equal to `CANONICAL_CHAIN_ID = 8453`. The guard `if (chainId != CANONICAL_CHAIN_ID) return address(0)` evaluates to `if (8453 != 8453)`, which is always false. `block.chainid` is never read anywhere in `src/`.

**Files:**

`src/OnChainLab.sol:618-623`, `src/factory/OnChainLabFactory.sol:220`.

**Impact:** Anyone can re-deploy the byte-identical CREATE2 stack on a non-canonical chain, mint a colliding tokenId, and `OnChainLab(addr).owner()` returns the attacker's address on that chain. Every `signer`-derived authorization (ERC-1271 fallback, `onlyEntryPointOrOwner`-gated functions, ERC-7739) is forgeable. The protocol's documented invariant ("chain ID matches deployment chain ID prevents cross-chain replay attacks") is structurally false.

**Proof of Concept:** Foundry test that PASSES against the in-tree codebase.

Add the following test to `test/solace-pocs/PoC_DeadChainIdGuard.t.sol`:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.33;

import {OnChainLabTestBase} from "test/base/OnChainLabTestBase.sol";
import {OnChainLab} from "src/OnChainLab.sol";
import {CANONICAL_CHAIN_ID} from "src/types/Constants.sol";

/// @title PoC: OnChainLab.owner() chain-id replay guard is dead code
/// @notice Demonstrates that the chain-id guard inside OnChainLab.owner() is structurally
///         unreachable. The factory always passes the constant `config.CANONICAL_CHAIN_ID()`
///         (= 8453) as the chainId argument when calling `ERC6551Registry.createAccount`
///         (`src/factory/OnChainLabFactory.sol:220`). The same constant is therefore
///         baked into the bytecode footer of every deployed account, so the read in
///         `token` always returns 8453 regardless of the chain the contract is
///         executing on. The check
///             if (chainId != CANONICAL_CHAIN_ID) return address(0);
///         (`src/OnChainLab.sol:620`) compares 8453 to 8453, which is always false.
/// @dev `block.chainid` is never read in src/. The NatSpec on owner() claims:
///         "First checks that the chain ID matches the deployment chain ID
///          This prevents cross-chain replay attacks where an account might be
///          used on a different chain"
///      That invariant is structurally violated.
contract PoC_DeadChainIdGuard is OnChainLabTestBase {
    function setUp() public override {
        // Bring up the full stack (forks Sepolia for EntryPoint/registry code).
        super.setUp();
    }

    /// @notice The chain-id guard inside owner() is dead code: regardless of
    ///         block.chainid, owner() returns the NFT owner instead of address(0).
    function test_PoC_DeadChainIdGuard() public {
        // ---------------------------------------------------------------
        // 1. Deploy the full stack normally on the Sepolia fork.
        //    Factory.createAccount embeds CANONICAL_CHAIN_ID = 8453 in the
        //    ERC-6551 bytecode footer, regardless of block.chainid.
        // ---------------------------------------------------------------
        vm.startPrank(user1);
        (address account, uint256 tokenId) = _mintAndCreateAccount(user1, bytes32(0));
        vm.stopPrank();

        // Sanity check: the account is bound to user1 right after creation.
        assertEq(labNft.ownerOf(tokenId), user1, "user1 must own the freshly minted NFT");
        assertEq(OnChainLab(payable(account)).owner(), user1, "owner() should return user1 in baseline");

        // Read the embedded chainId from the account's bytecode footer; this
        // value is what owner() compares against CANONICAL_CHAIN_ID.
        (uint256 footerChainId, address footerToken, uint256 footerTokenId) = OnChainLab(payable(account)).token();
        assertEq(footerChainId, CANONICAL_CHAIN_ID, "footer chainId is the constant 8453, not block.chainid");
        assertEq(footerToken, address(labNft), "footer token contract matches LabNFT proxy");
        assertEq(footerTokenId, tokenId, "footer tokenId matches minted tokenId");

        // ---------------------------------------------------------------
        // 2. Switch the EVM chainId to 1 (Ethereum mainnet - NOT canonical).
        //    The "documented" guard claims this should make owner() return
        //    address(0). It does not, because the comparison is 8453 != 8453.
        // ---------------------------------------------------------------
        vm.chainId(1);
        assertEq(block.chainid, 1, "vm.chainId did not change block.chainid");
        assertTrue(block.chainid != CANONICAL_CHAIN_ID, "we are on a non-canonical chain");

        // ---------------------------------------------------------------
        // 3. Call owner() on the deployed account.
        // ---------------------------------------------------------------
        address ownerOnChain1 = OnChainLab(payable(account)).owner();

        // ---------------------------------------------------------------
        // 4. Assert owner() returns the NFT owner (NOT address(0)).
        //    This is the smoking gun: the cross-chain replay guard is bypassed.
        // ---------------------------------------------------------------
        assertEq(
            ownerOnChain1,
            user1,
            "owner() returned the NFT owner on a non-canonical chain (guard is dead code)"
        );
        assertTrue(ownerOnChain1 != address(0), "owner() did NOT return address(0) - guard never fires");

        // ---------------------------------------------------------------
        // 5. Repeat for an arbitrary, completely unrelated chainId.
        //    The footer is immutable bytecode so the result is identical.
        // ---------------------------------------------------------------
        vm.chainId(999_999_999);
        assertEq(
            OnChainLab(payable(account)).owner(),
            user1,
            "owner() still returns NFT owner on chainId 999_999_999 - guard is structurally dead"
        );

        // ---------------------------------------------------------------
        // 6. Assert the structural invariant the NatSpec claims.
        //    "chain ID matches the deployment chain ID prevents cross-chain
        //     replay attacks". The footer chainId is the *constant*, never
        //     the deployment chain id, so this property cannot hold.
        // ---------------------------------------------------------------
        // The footer chainId equals the constant on every chain.
        (uint256 footerChainIdAfter,,) = OnChainLab(payable(account)).token();
        assertEq(footerChainIdAfter, CANONICAL_CHAIN_ID, "footer chainId is the constant baked at deploy time");
        // block.chainid differs from that constant in this scenario.
        assertTrue(
            block.chainid != footerChainIdAfter,
            "block.chainid != footer chainId - yet owner() does not return address(0)"
        );
        // Therefore the documented invariant
        //   "owner() returns address(0) on a non-canonical chain"
        // is violated.
    }
}
```

Run with: `forge test --match-test test_PoC_DeadChainIdGuard -vvv`

**Recommended Mitigation:** Replace `if (chainId != CANONICAL_CHAIN_ID)` with `if (block.chainid != CANONICAL_CHAIN_ID)`, or check both: `if (block.chainid != CANONICAL_CHAIN_ID || chainId != CANONICAL_CHAIN_ID)`.

**Molecule:** Acknowledged
