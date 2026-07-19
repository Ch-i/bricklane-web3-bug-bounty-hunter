---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-06-cyfrin-wlfi-unlock-v2-0-1-6
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-05-06T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-06-cyfrin-wlfi-unlock-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-06-cyfrin-wlfi-unlock-v2-0
title: '`WorldLibertyFinancialVester::ownerSetCategoryTemplate` does not enforce sum
  of `percentageOfAllocation` across templates, allowing misconfiguration to permanently
  strand user allocation'
vuln_class: []
---

# `WorldLibertyFinancialVester::ownerSetCategoryTemplate` does not enforce sum of `percentageOfAllocation` across templates, allowing misconfiguration to permanently strand user allocation

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-06-cyfrin-wlfi-unlock-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-06-cyfrin-wlfi-unlock-v2.0.md)_

---

**Description:** `WorldLibertyFinancialVester::ownerSetCategoryTemplate` performs index-bound and timestamp-ordering checks but does not constrain `percentageOfAllocation` bounds, nor does it validate that the sum of percentages across all templates in a category equals (or is ≤) `MAX_PERCENTAGE (= 1 ether)`:

```solidity
// WorldLibertyFinancialVester.sol
function ownerSetCategoryTemplate(
    uint8 _category,
    uint8 _index,
    Template calldata _template
) external onlyWorldLibertyOwner(msg.sender) {
    if (_index >= MAX_TEMPLATE_COUNT) { revert InvalidTemplateCount(); }
    if (_template.endTimestamp != 0) {
        if (_template.startTimestamp > _template.cliffTimestamp
            || _template.cliffTimestamp > _template.endTimestamp) {
            revert InvalidTemplateTimestamp();
        }
    }
    VesterStorage storage $ = _getStorage();
    $.categoryTemplates[_category][_index] = _template; // @audit accepts any percentage; no sum check
    uint8 count = $.categoryInfo[_category].templateCount;
    if (_index >= count) {
        count = _index + 1;
        $.categoryInfo[_category].templateCount = count;
        ...
    }
    ...
}
```

The `_unlockedTotal` math in the same contract uses a `remainingCap` mechanic that clamps the total unlocked amount at `allocation` when `sum(percentages) > 1 ether`. Concretely, if the sum is `< 1 ether`, the missing fraction `(1 ether - sum)` of every user's allocation becomes **permanently unclaimable** — `_unlockedTotal` never produces an `unlocked` value exceeding `sum * allocation / 1 ether`, so `claimable = unlocked - claimed` caps out strictly below `allocation`.


```solidity
// WorldLibertyFinancialVester.sol
function _unlockedTotal(
    VesterStorage storage $,
    uint8 _category,
    uint112 _allocation
) internal view returns (uint256) {
    ...
    uint256 remainingCap = _allocation;
    for (uint8 i; i < count; ) {
        Template memory template = $.categoryTemplates[_category][i];
        uint256 segmentCap = _allocation * uint256(template.percentageOfAllocation) / MAX_PERCENTAGE;
        segmentCap = segmentCap < remainingCap ? segmentCap : remainingCap;
        if (segmentCap != 0) {
            uint256 unlocked = _segmentUnlocked(template, segmentCap);
            totalUnlocked += unlocked;
            remainingCap -= segmentCap; // @audit if sum<1e18, loop ends with remainingCap > 0 permanently
            if (remainingCap == 0) { break; }
        }
        unchecked { ++i; }
    }
    return totalUnlocked;
}
```

**Impact:** Any owner action that writes a template resulting in a category's total coverage < `1 ether` permanently strands `(1 ether - sum) * allocation / 1 ether` of every user's allocation activated under that category. `ownerSetCategoryTemplate` is the ongoing admin surface for category configuration — every single-slot write, every future update, and every fix after V3 ships goes through this function without any safety net.


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

  describe('ownerSetCategoryTemplate sum-of-percentages gap', () => {
    it('permanently strands allocation when sum(percentageOfAllocation) < 1 ether', async function () {
      const wlfi = await impersonateReq(ctx.wlfi, true);
      const user = ctx.core.hhUser1;

      // Configure cat 2 with ONLY 50% coverage (NO second template to fill the rest)
      await ctx.vester.connect(ctx.wlfiOwner).ownerSetCategoryEnabled(Number(DEFAULT_CATEGORY), true);
      await ctx.vester.connect(ctx.wlfiOwner).ownerSetCategoryTemplate(Number(DEFAULT_CATEGORY), 0, {
        percentageOfAllocation: parseEther('0.5'),   // 50%
        startTimestamp: ZERO_BI,
        cliffTimestamp: ZERO_BI,
        endTimestamp: ZERO_BI,   // immediate unlock
      });

      // Activate user with 100 WLFI
      await ctx.wlfi.connect(ctx.wlfiOwner).transfer(user.address, DEFAULT_AMOUNT);
      await ctx.wlfi.connect(user).approve(ctx.vester, DEFAULT_AMOUNT);
      await ctx.vester.connect(wlfi).wlfiActivateVest(user.address, Number(DEFAULT_CATEGORY), DEFAULT_AMOUNT);

      await advanceTimeToAfterStartTimestamp(ctx);

      // Claimable should be capped at 50% of allocation
      expect(await ctx.vester.claimable(user.address)).to.eq(DEFAULT_AMOUNT / 2n);

      // User claims max
      await ctx.vester.connect(wlfi).wlfiClaimFor(user.address);

      // 50% has been claimed; the other 50% is PERMANENTLY STRANDED in Vester
      expect(await ctx.vester.claimed(user.address)).to.eq(DEFAULT_AMOUNT / 2n);
      expect(await ctx.vester.unclaimed(user.address)).to.eq(DEFAULT_AMOUNT / 2n);

      // Subsequent claim reverts with NothingToClaim — proof the remaining 50% is unreachable
      await expectThrowWithCustomError(
        ctx.vester.connect(wlfi).wlfiClaimFor(user.address),
        ctx.vester,
        'NothingToClaim',
      );

      // Even after a long time, no new unlock — template math caps at 50%
      await time.increase(86_400 * 365 * 10); // 10 years
      await expectThrowWithCustomError(
        ctx.vester.connect(wlfi).wlfiClaimFor(user.address),
        ctx.vester,
        'NothingToClaim',
      );
      expect(await ctx.vester.unclaimed(user.address)).to.eq(DEFAULT_AMOUNT / 2n);
    });
  });

});

```

**Recommended Mitigation:** Consider enforcing the sum invariant inside `ownerSetCategoryTemplate`.

```diff
function ownerSetCategoryTemplate(
    uint8 _category,
    uint8 _index,
    Template calldata _template
) external onlyWorldLibertyOwner(msg.sender) {

 ...
 VesterStorage storage $ = _getStorage();
    $.categoryTemplates[_category][_index] = _template;

    uint8 count = $.categoryInfo[_category].templateCount;
    if (_index >= count) {
        count = _index + 1;
        $.categoryInfo[_category].templateCount = count;
        emit SetCategoryTemplateCount(_category, count);

++    uint256 total;
++    for (uint8 i; i < count; i++) {
++        total += $.categoryTemplates[_category][i].percentageOfAllocation;
++   }
++    if (total > MAX_PERCENTAGE) {
++       revert InvalidTemplateSum();
++    }
        emit SetCategoryTemplate(_category, _index, _template);
    }
}
```

**WLFI:** Fixed in commit [1430e24](https://github.com/worldliberty/usd1-protocol/commit/1430e245349795921bebe275f6bd1d835d9f8fa3).

**Cyfrin:** Verified.
