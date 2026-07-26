---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-02-cyfrin-syntetika-ccip-cct-v2-0-0-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-05-02T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-02-cyfrin-syntetika-ccip-cct-v2-0
title: '`Minter::realizeLosses` is dead by default: reverts on missing vault to `Minter`
  allowance'
vuln_class: []
---

# `Minter::realizeLosses` is dead by default: reverts on missing vault to `Minter` allowance

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md)_

---

**Description:** `Minter::realizeLosses` calls `hilSyntheticToken.burnFrom(address(vault), lossesAmount)`. In `HilToken::burnFrom` the allowance check is skipped only when `spender == from` or `spender == owner()`. Here `spender == Minter`, `from == StakingVault`, and `owner() == initialAdmin` (distinct from the Minter proxy). Thus `_spendAllowance(vault, Minter, amount)` executes - the StakingVault never approves the Minter. No `approve` call from StakingVault to Minter exists in any deploy script or in `StakingVault::initialize`, and no function on `StakingVault` (or elsewhere reachable by admin) grants this allowance. Default allowance = 0 -> `ERC20InsufficientAllowance` revert for any non-zero loss.

This is distinct from the client-acknowledged "realizeLosses front-run DoS" known issue. Front-running implies the function normally works but can be perturbed; this finding shows the function can NEVER work in a standard deployment.

Source: `issuance/src/minter/Minter.sol:431-440`.

**Impact:** The protocol's only loss-realization path is unusable. The vault can only grow (yield minted) and never shrink to reflect custody losses, producing permanent over-collateralization drift and mispricing `sharePrice` during real losses. Admin's only alternative is a full protocol upgrade - exactly the destructive control the 2-step admin was meant to prevent.

**Proof of Concept:**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import "forge-std/Test.sol";
import {Minter} from "../../src/minter/Minter.sol";
import {HilBTC} from "../../src/token/HilBTC.sol";
import {HilToken} from "../../src/token/HilToken.sol";
import {StakingVault} from "../../src/vault/StakingVault.sol";
import {Distributor} from "../../src/vault/Distributor.sol";
import {MockFeed} from "../../src/vault/MockFeed.sol";
import {IStakingVault} from "../../src/interfaces/vault/IStakingVault.sol";
import {IFeed} from "../../src/interfaces/chainlink/IFeed.sol";
import {IMinter} from "../../src/interfaces/minter/IMinter.sol";
import {MockERC20} from "../mocks/MockERC20.sol";
import {MockPolicyEngine} from "../../src/kyc/MockPolicyEngine.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {
    ERC1967Proxy
} from "@openzeppelin/contracts/proxy/ERC1967/ERC1967Proxy.sol";

contract H02_RealizeLossesDead is Test {
    HilBTC hilBTC;
    MockERC20 baseAsset;
    StakingVault vault;
    Minter minter;
    Distributor distributor;
    MockFeed feed;

    address admin = address(0x1111);
    address custodian = address(0x2222);
    address operator = address(0x3333);
    address pauser = address(0x4444);
    address user1 = address(0x5555);

    function setUp() public {
        vm.warp(1770880586);
        vm.startPrank(admin);

        baseAsset = new MockERC20();

        HilBTC hilImpl = new HilBTC();
        bytes memory hilInit = abi.encodeWithSelector(
            HilToken.initialize.selector,
            "HilBTC",
            "hilBTC",
            admin,
            address(0)
        );
        ERC1967Proxy hilProxy = new ERC1967Proxy(address(hilImpl), hilInit);
        hilBTC = HilBTC(address(hilProxy));

        StakingVault vaultImpl = new StakingVault();
        bytes memory vaultInit = abi.encodeWithSelector(
            StakingVault.initialize.selector,
            IERC20(address(hilBTC)),
            "Staked HilBTC",
            "sHilBTC",
            admin,
            1_000,
            address(0)
        );
        ERC1967Proxy vaultProxy = new ERC1967Proxy(
            address(vaultImpl),
            vaultInit
        );
        vault = StakingVault(address(vaultProxy));

        Minter minterImpl = new Minter();
        MockPolicyEngine policyEngine = new MockPolicyEngine();
        bytes memory minterInit = abi.encodeWithSelector(
            Minter.initialize.selector,
            admin,
            address(baseAsset),
            address(hilBTC),
            custodian,
            operator,
            pauser,
            admin,
            address(policyEngine),
            IStakingVault(address(vault))
        );
        ERC1967Proxy minterProxy = new ERC1967Proxy(
            address(minterImpl),
            minterInit
        );
        minter = Minter(address(minterProxy));

        hilBTC.requestMinterChange(address(minter));
        hilBTC.setMinter();

        Distributor distrImpl = new Distributor();
        feed = new MockFeed();
        bytes memory distrInit = abi.encodeWithSelector(
            Distributor.initialize.selector,
            admin,
            IFeed(address(feed)),
            IMinter(address(minter)),
            8 hours
        );
        ERC1967Proxy distrProxy = new ERC1967Proxy(
            address(distrImpl),
            distrInit
        );
        distributor = Distributor(address(distrProxy));

        vault.setDistributor(address(minter));

        minter.requestDistributorChange(address(distributor));
        vm.warp(block.timestamp + 2 days);
        minter.setDistributor();

        vault.setCooldownDuration(0);

        minter.whitelistAddress(admin, true);
        minter.whitelistAddress(user1, true);

        vm.stopPrank();

        baseAsset.mint(admin, 1_000e8);
        baseAsset.mint(user1, 1_000e8);

        vm.prank(admin);
        baseAsset.approve(address(minter), type(uint256).max);

        vm.prank(user1);
        baseAsset.approve(address(minter), type(uint256).max);

        vm.startPrank(admin);
        minter.mint(admin, 500e8);
        hilBTC.approve(address(vault), type(uint256).max);
        vault.stake(100e8, "");
        vm.stopPrank();

        vm.startPrank(user1);
        minter.mint(user1, 500e8);
        hilBTC.approve(address(vault), type(uint256).max);
        vault.stake(200e8, "");
        vm.stopPrank();

        vm.prank(admin);
        feed.setYieldAmount(50e8);
        distributor.distributeYield();

        assertGt(hilBTC.balanceOf(address(vault)), 0, "vault has no hilBTC");
    }

    function test_PoC_realizeLossesRevertsDueToMissingAllowance() public {
        uint256 lossesAmount = 25e8;

        assertEq(
            hilBTC.allowance(address(vault), address(minter)),
            0,
            "vault unexpectedly pre-approved minter"
        );

        vm.prank(admin);
        vm.expectRevert();
        distributor.realizeLosses(lossesAmount);

        vm.startPrank(admin);
        minter.requestDistributorChange(admin);
        vm.warp(block.timestamp + 2 days);
        minter.setDistributor();
        vm.expectRevert();
        minter.realizeLosses(lossesAmount);
        vm.stopPrank();
    }

    function test_PoC_realizeLossesWorksAfterAllowance() public {
        uint256 lossesAmount = 25e8;
        uint256 vaultBalBefore = hilBTC.balanceOf(address(vault));

        vm.prank(address(vault));
        hilBTC.approve(address(minter), type(uint256).max);

        vm.prank(admin);
        distributor.realizeLosses(lossesAmount);

        uint256 vaultBalAfter = hilBTC.balanceOf(address(vault));
        assertEq(
            vaultBalBefore - vaultBalAfter,
            lossesAmount,
            "vault hilBTC not burned by expected amount"
        );
    }
}
```

Both test cases pass: the first confirms `ERC20InsufficientAllowance(Minter, 0, lossesAmount)` on both the `Distributor::realizeLosses -> Minter::realizeLosses` path and the direct `Minter::realizeLosses` path; the second shows the function works only after simulating a vault-side approve, which no admin function currently exposes (requires a proxy upgrade).

**Recommended Mitigation:** Either:
- Have StakingVault grant Minter `forceApprove(minter, type(uint256).max)` during initialization; or
- Change `realizeLosses` to have the vault burn its own balance via an `onlyMinter` function on the vault; or
- In `HilToken::burnFrom`, skip allowance when `spender == $.minter` (treat the minter role as privileged for `burnFrom` like owner).

**Syntetika:** Fixed in commit [`9cdb8d7`](https://github.com/SyntetikaLabs/monorepo/commit/9cdb8d745a8b3279a188639a0ee7958b63b68f44)

**Cyfrin:** Verified. Allowance skipped when `spender` is `minter`


\clearpage
