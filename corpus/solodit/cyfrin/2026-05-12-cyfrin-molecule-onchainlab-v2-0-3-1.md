---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-12-cyfrin-molecule-onchainlab-v2-0-3-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-05-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-12-cyfrin-molecule-onchainlab-v2-0
title: '`LabNFT::transferFrom, mint` bypass circular-ownership invariant'
vuln_class: []
---

# `LabNFT::transferFrom, mint` bypass circular-ownership invariant

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-12-cyfrin-molecule-onchainlab-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md)_

---

**Description:** The protective revert in `OnChainLab::onERC721Received` only fires on safe-transfer paths. Two paths bypass it. First, the Solady ERC-721 unsafe transfer path does NOT invoke `onERC721Received`, so most marketplace settlement transfers can land the LabNFT in its own bound account. Second, `LabNFT.mint(predicted)` and `OnChainLabFactory.mintAndCreateAccount(predicted)` call Solady `_mint` which also skips the receive hook, locking a fresh tokenId at its bound account permanently. The bound account address is computable pre-mint via `OclDerivationConfig.accountOf(tokenId)`.

**Files:**

`src/OnChainLab.sol:553-564`, `src/NFT/LabNFT.sol:82-89`. LabNFT uses Solady ERC-721 and does not override the unsafe transfer path.

**Impact:** Once `LabNFT.ownerOf(T)` returns the bound account address, `OnChainLab::owner` returns the bound account, `signer` returns the bound account, `RootValidator::validateUserOp` requires recovery to the bound account (a contract with no key), and `execute` requires `msg.sender == signer()`. The account is permanently inert and any assets it holds are unrecoverable. The documented invariant in the README ("circular ownership: onERC721Received check prevents LabNFT from being sent to its own bound account") is structurally false.

**Proof Of Concept:**
Run the following PoC:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.33;

import {OnChainLabTestSetup} from "test/base/OnChainLabTestSetup.sol";
import {OnChainLab} from "src/OnChainLab.sol";
import {IEntryPoint} from "src/interfaces/IEntryPoint.sol";
import {LabNFT} from "src/NFT/LabNFT.sol";
import {ERC1967Proxy} from "@openzeppelin-contracts-5.6.0/proxy/ERC1967/ERC1967Proxy.sol";
import {ERC6551Registry} from "src/core/ERC6551Registry.sol";
import {ERC7484Registry} from "src/ERC7484Registry/ERC7484Registry.sol";
import {RootValidator} from "src/modules/validator/RootValidator.sol";
import {MockCallContract} from "test/mock/MockCallContract.sol";
import {MockExecutor} from "test/mock/MockExecutor.sol";
import {MockFallback} from "test/mock/MockFallback.sol";

contract PoC_CircularOwnership is OnChainLabTestSetup {
    function setUp() public override {
        sepoliaFork = vm.createFork(vm.envString("SEPOLIA_RPC"));
        vm.selectFork(sepoliaFork);

        entryPoint = IEntryPoint(payable(0x4337084D9E255Ff0702461CF8895CE9E3b5Ff108));
        assertTrue(address(entryPoint).code.length > 0);

        deployer = makeAddr("Deployer");
        (user1, user1PrivateKey) = makeAddrAndKey("User1");
        bundler = makeAddr("Bundler");
        moleculeRegistryAttestor = makeAddr("MoleculeRegistryAttestor");

        vm.startPrank(deployer);
        LabNFT labNftImpl = new LabNFT();
        ERC1967Proxy labNftProxy = new ERC1967Proxy(address(labNftImpl), abi.encodeCall(LabNFT.initialize, (deployer)));
        labNft = LabNFT(address(labNftProxy));
        erc6551Registry = new ERC6551Registry();
        erc7484registry = new ERC7484Registry();
        rootValidator = new RootValidator();
        _deployFactory();
        mockCallContract = new MockCallContract();
        mockExecutor = new MockExecutor();
        mockFallback = new MockFallback();
        mockFallback2 = new MockFallback();
        vm.stopPrank();
    }


    function test_PoC_TransferFromToBoundAccount_Locks() public {
        // user1 mints tokenId 0 to themselves and creates the bound account
        vm.startPrank(user1);
        labNft.mint(user1);
        accountProxy = _createAndInitializeAccount(bytes32(0), 0, true);
        vm.stopPrank();

        assertEq(labNft.ownerOf(0), user1);
        assertEq(OnChainLab(payable(accountProxy)).owner(), user1);

        // Now use unsafe transferFrom to send the NFT TO its bound account.
        // onERC721Received is NOT invoked → SelfOwnershipNotAllowed never fires.
        vm.prank(user1);
        labNft.transferFrom(user1, accountProxy, 0);

        assertEq(labNft.ownerOf(0), accountProxy, "NFT now owned by its own bound account");
        assertEq(OnChainLab(payable(accountProxy)).owner(), accountProxy, "owner() == self (bricked)");
        assertEq(OnChainLab(payable(accountProxy)).signer(), accountProxy, "signer() == self (bricked)");
    }


}

```

**Recommended Mitigation:** Override Solady's pre-transfer hook on `LabNFT` to revert when the destination address equals the bound account derived from the tokenId via `derivationConfig.accountOf(tokenId)`. This catches the unsafe transfer path, `safeTransferFrom`, and `_mint` uniformly.

**Molecule:** Fixed in [f4cc44b](https://github.com/moleculeprotocol/onchainlabs/commit/f4cc44b).

**Cyfrin:** Verified.
