---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-2-3
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-05-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-13-cyfrin-armada-crowdfund-governance-v2-0
title: '`ArmadaCrowdfund::finalize` refunds raises above `MIN_SALE` when 67-99 hop-0
  participants but sale succeeds when 100+ hop-0 participants'
vuln_class: []
---

# `ArmadaCrowdfund::finalize` refunds raises above `MIN_SALE` when 67-99 hop-0 participants but sale succeeds when 100+ hop-0 participants

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** `ArmadaCrowdfund::finalize` forces `refundMode` on raises that cleared the public-facing `MIN_SALE` threshold. A hop-0-concentrated raise with 67-99 seeds (each committing the per-seed cap of `$15,000`) produces `cappedDemand` between `$1,005,000` and `$1,485,000` — all above the `$1,000,000` `MIN_SALE` — and is refunded anyway. Adding one more seed (`99 → 100`) flips the outcome from refund to success, because 100 seeds at `$15K` each produces `cappedDemand = $1,500,000` which trips the `ELASTIC_TRIGGER` and expands `saleSize` to `MAX_SALE`, lifting `hop0Ceiling` above `MIN_SALE`. The cliff is non-monotonic and counterintuitive to participants: every outcome in the dead zone is equally refunded regardless of how far above `MIN_SALE` the commitment climbed, but one more seed tips the raise into success.

| Hop-0 seeds (each at `$15K` cap) | `cappedDemand` | `saleSize` | `hop0Ceiling` | Outcome |
|---|---|---|---|---|
| ≤ 66 | ≤ `$990,000` | BASE = `$1.2M` | `$798K` | `refundMode` — gate 1 fails (expected) |
| **67-99** | **`$1,005,000`-`$1,485,000`** | **BASE = `$1.2M`** | **`$798K`** | **`refundMode` — gate 2 fails (the bug)** |
| 100-160 (cap) | `$1,500,000`-`$2,400,000` | MAX = `$1.8M` (elastic) | `$1,197K` | Success |

**Mechanism:**

`finalize` at `contracts/crowdfund/ArmadaCrowdfund.sol:392-441` has two `MIN_SALE` gates that test incomparable quantities:

```solidity
// Gate 1: pre-allocation, on aggregate capped demand
_computeCappedDemand();
if (cappedDemand < MIN_SALE) { refundMode = true; ...; return; }

// (elastic decision, then _computeHopAllocations produces totalAllocUsdc_)

// Gate 2: post-allocation, on ceiling-clamped allocations
if (totalAllocUsdc_ < MIN_SALE) { refundMode = true; ...; return; }
```

`cappedDemand` applies the per-participant `cap` (`min(committed, effectiveCap)`) and sums — it is the aggregate commitment to the sale. `totalAllocUsdc_` additionally applies each hop's `ceiling` on top of demand and sums. "Cap" and "ceiling" are distinct constraints:

- **Per-participant cap** (`effectiveCap = $15K` at hop-0): prevents any single participant from taking too much.
- **Per-hop ceiling** (`hop0Ceiling = $798K` under BASE_SALE): prevents any single hop from consuming more than its share of `saleSize`.

Because `hop0Ceiling ($798K) < MIN_SALE ($1M)`, a hop-0-concentrated raise that clears gate 1 always fails gate 2 unless hop-1 or hop-2 demand fills the `$202K` gap between the ceiling and `MIN_SALE`. The `ELASTIC_TRIGGER = $1,500,000` boundary is the only way to lift `hop0Ceiling` above `MIN_SALE` under this allocation structure, which is why `67-99` seeds refund but 100 seeds succeed.

**Impact:** Any hop-0-concentrated raise in the 67-99 seed dead zone (or equivalent mixed-hop distribution where the hop-1/hop-2 contribution falls short of `$202K`) is forced into `refundMode` despite meeting the commitment threshold: participants recover their USDC via `claimRefund`, no ARM is distributed, and the pre-loaded `MAX_SALE × 1e12 ARM` stays in the contract for `withdrawUnallocatedArm`. Participants who committed above the promised `MIN_SALE` believe they participated in a successful raise and are instead refunded, producing a surprising outcome that the participant-facing `MIN_SALE` promise cannot predict from commitment totals alone.

**Proof of Concept:** Add the following test to `test-foundry/solace-pocs/PoC_L_MinSaleDisparity.t.sol`:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import "forge-std/Test.sol";
import "../../contracts/crowdfund/ArmadaCrowdfund.sol";
import "../../contracts/crowdfund/IArmadaCrowdfund.sol";
import "../../contracts/governance/ArmadaToken.sol";
import "../../contracts/cctp/MockUSDCV2.sol";

contract PoC_MinSaleDisparityTest is Test {
    ArmadaCrowdfund public crowdfund;
    MockUSDCV2 public usdc;
    ArmadaToken public armToken;

    address public admin;
    address public treasury;

    uint256 constant ARM_FUNDING  = 1_800_000 * 1e18;
    uint256 constant TOTAL_SEEDS  = 100;
    uint256 constant SEED_COMMIT  = 15_000 * 1e6;

    address[] seeds;

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

        // Add and fund all 100 seeds. Seed 100 stays uncommitted at snapshot time.
        seeds = new address[](TOTAL_SEEDS);
        address[] memory seedArr = new address[](TOTAL_SEEDS);
        for (uint256 i = 0; i < TOTAL_SEEDS; i++) {
            seeds[i] = address(uint160(0x1000 + i));
            seedArr[i] = seeds[i];
            usdc.mint(seeds[i], SEED_COMMIT);
        }
        crowdfund.addSeeds(seedArr);

        for (uint256 i = 0; i < 99; i++) {
            vm.startPrank(seeds[i]);
            usdc.approve(address(crowdfund), SEED_COMMIT);
            crowdfund.commit(0, SEED_COMMIT);
            vm.stopPrank();
        }
    }

    function test_PoC_OneMoreSeedFlipsRefundToSuccess() public {
        // Snapshot state after 99 commits, before finalize
        uint256 snapshotId = vm.snapshotState();

        // === Scenario 1: finalize with 99 committed seeds → refundMode ===
        vm.warp(crowdfund.windowEnd() + 1);
        crowdfund.finalize();

        assertEq(crowdfund.cappedDemand(), 1_485_000 * 1e6);
        assertGe(crowdfund.cappedDemand(), crowdfund.MIN_SALE(), "gate 1 passed");
        assertEq(crowdfund.saleSize(), crowdfund.BASE_SALE());
        assertEq(crowdfund.saleSize(), 1_200_000 * 1e6);
        assertTrue(crowdfund.refundMode(), "99 seeds: refundMode triggered");
        assertEq(crowdfund.totalAllocatedUsdc(), 0);

        // === Revert to snapshot: 99 commits remain, 100th still uncommitted ===
        require(vm.revertToState(snapshotId), "revertToState failed");
        assertEq(uint256(crowdfund.phase()), uint256(Phase.Active));
        assertEq(crowdfund.cappedDemand(), 0);
        assertFalse(crowdfund.refundMode());

        // === Scenario 2: seed 100 commits, finalize → sale succeeds ===
        vm.startPrank(seeds[99]);
        usdc.approve(address(crowdfund), SEED_COMMIT);
        crowdfund.commit(0, SEED_COMMIT);
        vm.stopPrank();

        vm.warp(crowdfund.windowEnd() + 1);
        crowdfund.finalize();

        assertEq(crowdfund.cappedDemand(), 1_500_000 * 1e6);
        assertEq(crowdfund.saleSize(), crowdfund.MAX_SALE());
        assertEq(crowdfund.saleSize(), 1_800_000 * 1e6);
        assertFalse(crowdfund.refundMode(), "100 seeds: sale succeeds");
        assertEq(crowdfund.totalAllocatedUsdc(), 1_197_000 * 1e6);
        assertEq(crowdfund.totalAllocatedArm(),  1_197_000 * 1e18);
    }
}
```

Run with:
```
forge test --match-test test_PoC_OneMoreSeedFlipsRefundToSuccess -vv
```

The test uses `vm.snapshotState` / `vm.revertToState` to demonstrate both sides of the cliff from identical pre-finalize state. Scenario 1 finalizes with 99 committed seeds: `cappedDemand = $1,485,000` clears gate 1, but `hop0Ceiling = $798,000 < MIN_SALE` fails gate 2, triggering `refundMode`. State reverts; seed 100 commits; finalize again. Scenario 2: `cappedDemand = $1,500,000` trips `ELASTIC_TRIGGER`, `saleSize` jumps to `MAX_SALE $1.8M`, `hop0Ceiling` becomes `$1,197,000 ≥ MIN_SALE`, gate 2 passes, sale succeeds. One additional committed seed flips refund → success.

**Recommended Mitigation:** Remove the post-allocation `MIN_SALE` gate. Gate 1 (`cappedDemand >= MIN_SALE`) is the authoritative interest threshold - it tests that enough participants committed to the sale. Gate 2 (`totalAllocUsdc_ >= MIN_SALE`) re-tests the same promise against ceiling-clamped allocations, which is not the same quantity; a raise that cleared the commitment threshold can fail this second test purely because of how ceilings distribute the allocation. Removing gate 2 preserves `MIN_SALE = $1M` as the meaningful raise target (promise kept to participants) while allowing ceiling-constrained raises that cleared the threshold to proceed.

```diff
 uint256 totalAllocUsdc_ = _computeHopAllocations(saleSize);

-// Post-allocation minimum raise check: if net proceeds (allocated USDC) fall
-// below MIN_SALE, enter refundMode. Participants get full USDC refunds via
-// claimRefund(); no ARM is distributed. This can occur at BASE_SALE when hop-0
-// is oversubscribed and later hops don't close the gap to $1M. Cannot occur
-// after expansion (hop-0 ceiling alone exceeds MIN_SALE).
-if (totalAllocUsdc_ < MIN_SALE) {
-    refundMode = true;
-    phase = Phase.Finalized;
-    finalizedAt = block.timestamp;
-    emit Finalized(saleSize, 0, 0, true);
-    return;
-}
-
 // Step 3: Store aggregate hop-level results.
```

After the fix, the 99-seed scenario proceeds normally: each seed receives its pro-rata ARM allocation (approximately `$8,060` worth at `$1/ARM`) plus a `$6,940` USDC refund; treasury receives the ceiling-clamped `$798,000` aggregate proceeds; unsold ARM stays in the contract, sweepable via `withdrawUnallocatedArm`. The 67-99 refund dead zone no longer exists; only raises that genuinely fail gate 1 (`cappedDemand < MIN_SALE`) enter `refundMode`.

**Test-suite update required alongside the code change.** Nine tests in `test-foundry/ArmadaCrowdfundRefundMode.t.sol` currently use the oversubscribed-hop-0 scenario (via `_allSeedsCommitFull()`) as the setup that triggers `refundMode`. These need their setups changed to trigger `refundMode` the other way (commit less than `MIN_SALE` at any hop so gate 1 fails). The specific test `test_refundMode_triggers_whenAllocBelowMinSale` should be removed entirely - it encodes the bug behavior. `test_claim_revertsInRefundMode`, `test_claimRefund_returnsFullUsdc_inRefundMode`, `test_computeAllocation_revertsInRefundMode`, `testFuzz_claimRefund_exactAmount`, and similar tests should have their setup helpers swapped to a commit-below-`MIN_SALE` variant.

**Armada:** Acknowledged.
