---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-06-cyfrin-wlfi-unlock-v2-0-1-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-05-06T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-06-cyfrin-wlfi-unlock-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-06-cyfrin-wlfi-unlock-v2-0
title: '`WorldLibertyFinancialVester::wlfiBurnAllocation` asserts `claimed <= allocation`
  post-burn, panicking on users who claimed more than 90% of their pre-election allocation'
vuln_class: []
---

# `WorldLibertyFinancialVester::wlfiBurnAllocation` asserts `claimed <= allocation` post-burn, panicking on users who claimed more than 90% of their pre-election allocation

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-06-cyfrin-wlfi-unlock-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-06-cyfrin-wlfi-unlock-v2.0.md)_

---

**Description:** `WorldLibertyFinancialVester::wlfiBurnAllocation` decrements `userInfo.allocation` by the requested amount, then asserts `userInfo.claimed <= userInfo.allocation`. When called during V3's team election, the burn amount is `allocation / 10`, so the post-burn allocation is `0.9 * old_allocation`. If the user has claimed more than that post-burn threshold (i.e., `claimed > 0.9 * old_allocation`), system panics.

```solidity
// WorldLibertyFinancialVester.sol
function wlfiBurnAllocation(address _user, uint256 _amount) external whenNotPaused {
    if (msg.sender != address(WLFI)) { revert Unauthorized(); }
    VesterStorage storage $ = _getStorage();
    UserInfo storage userInfo = $.users[_user];
    userInfo.allocation -= uint112(_amount); // post-burn: 0.9 * old_allocation
    assert(userInfo.claimed <= userInfo.allocation); // @audit panics when claimed > 0.9*old_allocation
    $.totalAllocated -= uint112(_amount);
    assert($.totalClaimed <= $.totalAllocated);
    WLFI.burn(_amount);
    ...
}
```

A single such user in a batched array aborts the entire transaction — rolling back the successful elections of every other user in the array.

```solidity
// WorldLibertyFinancialV3.sol
function ownerElectVestingUpdatesFor(address[] calldata _accounts) external onlyOwner {
    for (uint256 i; i < _accounts.length; ++i) {
        _electVestingUpdate(_accounts[i]); // @audit any revert here aborts the entire loop
    }
}
```

For the user in isolation (user-path `electVestingUpdate(sig)` or owner-path on a single address), the same panic blocks the election entirely — the user cannot transition to cat 47 via any path.

As per scope, the governance proposal's 10-day election cap was removed — elections are open indefinitely with only state-based replay protection (`ElectionAlreadyPerformed`). Without a deadline, any user who eventually claims >90% of their pre-election allocation becomes permanently un-electable and permanently poisons any batch that includes them. The bug's population grows monotonically as long as old-category templates continue vesting and elections remain pending.


**Impact:** A high-claimed team user cannot be elected into cat 47 at all — not by the owner, not by their own signed message. Also, a single "poisoned" user in a batch of 500 aborts the entire batch. The owner must identify the offender off-chain (from the bare `Panic(0x01)` — no custom error payload identifies the user), remove them, and retry.


**Proof of Concept:** Run the following test:

```typescript
import { loadFixture, time } from '@nomicfoundation/hardhat-network-helpers';
import { expect } from 'chai';
import { parseEther } from 'ethers';
import { impersonateReq } from '../../script/execution-utils';
import { ONE_ETH_BI, ZERO_BI } from '../../src/no-dependencies-constants';
import { IWorldLibertyFinancialVester } from '../../src/types';
import { FinalizedVestingCategory, WLFI_START_TIMESTAMP } from '../../src/wlfi-constants';
import { deployWlfiV2Fixture } from '../fixtures';
import { expectEvent, expectThrowWithCustomError } from '../utils';
import { advanceTimeToAfterStartTimestamp } from '../wlfi/wlfi-utils';

type Ctx = Awaited<ReturnType<typeof deployWlfiV2Fixture>>;
let ctx: Ctx;

const DEFAULT_AMOUNT = parseEther('100');
const DEFAULT_CATEGORY = 2n;

// An immediate-unlock template: endTimestamp = 0 means "fully unlocked regardless of time"
const IMMEDIATE_TEMPLATE: IWorldLibertyFinancialVester.TemplateStruct = {
  percentageOfAllocation: parseEther('1'),
  startTimestamp: ZERO_BI,
  cliffTimestamp: ZERO_BI,
  endTimestamp: ZERO_BI,
};

describe('WorldLibertyFinancialVester — Edge Cases (audit)', () => {
  beforeEach(async () => {
    ctx = await loadFixture(deployWlfiV2Fixture);
  });


  describe('wlfiBurnAllocation assert panic on over-claimed user (Vester Finding [*Duplicated `WLFI` access control check can be extracted into a modifier*](#duplicated-wlfi-access-control-check-can-be-extracted-into-a-modifier))', () => {
    it('panics when userInfo.claimed > userInfo.allocation - _amount', async function () {
      const wlfi = await impersonateReq(ctx.wlfi, true);
      const user = ctx.core.hhUser1;

      // Set up cat 2 with immediate 100% unlock
      await ctx.vester.connect(ctx.wlfiOwner).ownerSetCategoryEnabled(Number(DEFAULT_CATEGORY), true);
      await ctx.vester.connect(ctx.wlfiOwner).ownerSetCategoryTemplate(
        Number(DEFAULT_CATEGORY), 0, IMMEDIATE_TEMPLATE,
      );

      // Activate user with 100 WLFI
      await ctx.wlfi.connect(ctx.wlfiOwner).transfer(user.address, DEFAULT_AMOUNT);
      await ctx.wlfi.connect(user).approve(ctx.vester, DEFAULT_AMOUNT);
      await ctx.vester.connect(wlfi).wlfiActivateVest(user.address, Number(DEFAULT_CATEGORY), DEFAULT_AMOUNT);

      await advanceTimeToAfterStartTimestamp(ctx);

      // User claims all 100 (immediate unlock template)
      await ctx.vester.connect(wlfi).wlfiClaimFor(user.address);
      expect(await ctx.vester.claimed(user.address)).to.eq(DEFAULT_AMOUNT);
      expect(await ctx.vester.allocation(user.address)).to.eq(DEFAULT_AMOUNT);

      // Snapshot state that should be unwound by the panic
      const allocBefore = await ctx.vester.allocation(user.address);
      const totalAllocBefore = await ctx.vester.totalAllocated();
      const totalSupplyBefore = await ctx.wlfi.totalSupply();

      // try to burn 10% of allocation.
      //   userInfo.allocation = 100; claimed = 100
      //   post-sub: allocation = 90; assert(claimed=100 <= allocation=90) -> FALSE -> panic
      const burnAmount = DEFAULT_AMOUNT / 10n;
      await expect(
        ctx.vester.connect(wlfi).wlfiBurnAllocation(user.address, burnAmount),
      ).to.be.reverted;
    });

  });

});

```

**Recommended Mitigation:** Consider a two-layer fix — safe-burn math in the Vester, per-user failure isolation in V3 via a try-catch in a self-call mode:

```diff
// File: contracts/wlfi/WorldLibertyFinancialVester.sol
function wlfiBurnAllocation(address _user, uint256 _amount) external whenNotPaused {
    if (msg.sender != address(WLFI)) { revert Unauthorized(); }
    VesterStorage storage $ = _getStorage();
    UserInfo storage userInfo = $.users[_user];

++    uint112 amount112 = uint112(_amount);
++    if (uint256(userInfo.claimed) + uint256(amount112) > uint256(userInfo.allocation)) {
++       revert ClaimedExceedsPostBurnAllocation(_user);
++    }

    userInfo.allocation -= amount112;
    // (assert can remain as belt-and-suspenders, but is now unreachable)
    assert(userInfo.claimed <= userInfo.allocation);
    ...
}
```

```diff
// WorldLibertyFinancialV3.sol
++ event ElectVestingUpdateFailed(address indexed account, bytes errorData);

++ function _tryElectVestingUpdate(address _account) external {
++    require(msg.sender == address(this), "self-only");
++   _electVestingUpdate(_account);
++ }

++ function ownerElectVestingUpdatesFor(address[] calldata _accounts) external onlyOwner {
++   for (uint256 i; i < _accounts.length; ++i) {
++        try this._tryElectVestingUpdate(_accounts[i]) {
++           // success
++        } catch (bytes memory errorData) {
++            emit ElectVestingUpdateFailed(_accounts[i], errorData);
++       }
++    }
++}
```


**WLFI:** Acknowledged. There are no users who have claimed non-zero tokens.
