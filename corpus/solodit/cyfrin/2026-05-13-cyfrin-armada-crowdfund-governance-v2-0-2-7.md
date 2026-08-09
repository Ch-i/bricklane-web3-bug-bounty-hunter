---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-2-7
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-05-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-13-cyfrin-armada-crowdfund-governance-v2-0
title: '`ArmadaCrowdfund::finalize` rounding buffer over-reserves USDC by factor of
  `NUM_HOPS`'
vuln_class: []
---

# `ArmadaCrowdfund::finalize` rounding buffer over-reserves USDC by factor of `NUM_HOPS`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** `ArmadaCrowdfund::finalize` at `contracts/crowdfund/ArmadaCrowdfund.sol:463` reserves a rounding buffer before pushing proceeds to treasury:

```solidity
uint256 roundingBuffer = participantNodes.length * NUM_HOPS;
```

The buffer covers floor-division loss in `_computeAllocation` where oversubscribed hops compute `allocUsdc = (cappedCommitted * finalCeilings[hop]) / finalDemands[hop]`. Each claim at one `(address, hop)` node loses at most one USDC unit. `participantNodes` already enumerates one entry per node, so the tight upper bound on total dust is `participantNodes.length * 1`. The `* NUM_HOPS` factor triple-counts and permanently strands `participantNodes.length * (NUM_HOPS - 1)` USDC units - no function can move contract USDC to treasury after finalize.

**Impact:** USDC collected from participants is locked in the contract instead of reaching treasury. For the practical cap of roughly 1,500 participant nodes, worst-case stranding is roughly 3,000 USDC units (roughly $0.003). Over-reserving never causes a refund shortfall, hence Low severity.

**Proof of Concept:** Add the following test to `test-foundry/solace-pocs/PoC_L_RoundingBufferOverReserve.t.sol`:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import "forge-std/Test.sol";
import "../../contracts/crowdfund/ArmadaCrowdfund.sol";
import "../../contracts/crowdfund/IArmadaCrowdfund.sol";
import "../../contracts/governance/ArmadaToken.sol";
import "../../contracts/cctp/MockUSDCV2.sol";

contract PoC_RoundingBufferOverReserveTest is Test {
    ArmadaCrowdfund public crowdfund;
    MockUSDCV2 public usdc;
    ArmadaToken public armToken;

    address public admin;
    address public treasury;

    uint256 constant ARM_FUNDING = 1_800_000 * 1e18;
    uint256 constant SEED_COUNT  = 100;            // hits ELASTIC_TRIGGER at $15k/seed
    uint256 constant SEED_COMMIT = 15_000 * 1e6;   // full hop-0 cap
    uint8   constant NUM_HOPS    = 3;

    function setUp() public {
        admin = address(this);
        treasury = address(0xCAFE);

        usdc = new MockUSDCV2("Mock USDC", "USDC");
        armToken = new ArmadaToken(admin, admin);
        crowdfund = new ArmadaCrowdfund(
            address(usdc), address(armToken), treasury,
            admin, admin, block.timestamp
        );

        address[] memory wl = new address[](2);
        wl[0] = admin;
        wl[1] = address(crowdfund);
        armToken.initWhitelist(wl);

        address[] memory delegators = new address[](1);
        delegators[0] = address(crowdfund);
        armToken.initAuthorizedDelegators(delegators);

        armToken.transfer(address(crowdfund), ARM_FUNDING);
        crowdfund.loadArm();
    }

    function _seed(uint256 i) internal pure returns (address) {
        return address(uint160(0x1000 + i));
    }

    function test_PoC_FinalizeOverReservesRoundingBuffer() public {
        address[] memory seeds = new address[](SEED_COUNT);
        for (uint256 i = 0; i < SEED_COUNT; i++) seeds[i] = _seed(i);
        crowdfund.addSeeds(seeds);

        for (uint256 i = 0; i < SEED_COUNT; i++) {
            usdc.mint(seeds[i], SEED_COMMIT);
            vm.startPrank(seeds[i]);
            usdc.approve(address(crowdfund), SEED_COMMIT);
            crowdfund.commit(0, SEED_COMMIT);
            vm.stopPrank();
        }

        vm.warp(crowdfund.windowEnd() + 1);
        crowdfund.finalize();
        assertFalse(crowdfund.refundMode());

        // Per-seed alloc: (15000 * 1197000) / 1500000 = 11970 (integer-exact, zero rounding)
        uint256 allocPerSeed = 11_970 * 1e6;
        uint256 totalAlloc   = SEED_COUNT * allocPerSeed;
        uint256 buffer       = SEED_COUNT * NUM_HOPS;
        assertEq(crowdfund.totalAllocatedUsdc(), totalAlloc);
        assertEq(usdc.balanceOf(treasury), totalAlloc - buffer);

        uint256 sumClaimed;
        for (uint256 i = 0; i < SEED_COUNT; i++) {
            vm.prank(seeds[i]);
            crowdfund.claim(seeds[i]);
            sumClaimed += allocPerSeed;
        }

        // Actual dust = 0; entire buffer stranded.
        assertEq(sumClaimed, crowdfund.totalAllocatedUsdc());
        assertEq(usdc.balanceOf(address(crowdfund)), buffer);
        assertEq(buffer - SEED_COUNT, SEED_COUNT * (NUM_HOPS - 1));
    }
}
```

Run with `forge test --match-test test_PoC_FinalizeOverReservesRoundingBuffer -vv`.

100 seeds each commit $15k at hop-0, triggering elastic expansion to `MAX_SALE = $1.8M`. Per-seed allocation is integer-exact (`11,970 USDC`), so actual dust is zero yet the contract retains the full 300-unit buffer after all claims.

**Recommended Mitigation:**
```diff
-uint256 roundingBuffer = participantNodes.length * NUM_HOPS;
+uint256 roundingBuffer = participantNodes.length;
```

Verified against the full forge suite: all 50 existing crowdfund tests pass, conservation invariants hold, and treasury recovers the previously stranded `participantNodes.length * (NUM_HOPS - 1)` USDC per sale.

**Armada:** Fixed in commit [a9680ce](https://github.com/ship-armada/armada-poc/commit/a9680ce9f0c6f07faeb50c0ed4667f7edd8b2833).

**Cyfrin:** Verified.
