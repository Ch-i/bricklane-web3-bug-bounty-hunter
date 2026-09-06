---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-06-cyfrin-wlfi-unlock-v2-0-1-7
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-05-06T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-06-cyfrin-wlfi-unlock-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-06-cyfrin-wlfi-unlock-v2-0
title: '`WorldLibertyFinancialRegistry::agentBulkInsertLegacyUsers` overwrite resets
  `isActivated=false`, freezing the user''s WLFI balance via V2''s `_update` gate'
vuln_class: []
---

# `WorldLibertyFinancialRegistry::agentBulkInsertLegacyUsers` overwrite resets `isActivated=false`, freezing the user's WLFI balance via V2's `_update` gate

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-06-cyfrin-wlfi-unlock-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-06-cyfrin-wlfi-unlock-v2.0.md)_

---

**Description:** `WorldLibertyFinancialRegistry::agentBulkInsertLegacyUsers` unconditionally writes the full `LegacyUser` struct with `isActivated: false` hardcoded, regardless of whether an entry for that user already exists:

```solidity
//WorldLibertyFinancialRegistry.sol
$.legacyUserMap[_users[i]] = LegacyUser({
    amount: uint112(_amounts[i]),
    category: _categories[i],
    isActivated: false  // @audit hardcoded — overwrites any prior activation
});
```
If a user has activated, claimed some amount (so their WLFI balance is non-zero again), and the agent subsequently re-inserts them — the balance-match check `WLFI.balanceOf(user) == _amounts[i]` passes (user's post-claim balance is non-zero), and the overwrite resets `isActivated` to `false`.

This state is toxic because `WorldLibertyFinancialV2::_update` refuses to transfer to/from a legacy-user-not-activated account after trading-start:

```solidity
// File: contracts/wlfi/WorldLibertyFinancialV2.sol
function _update(address _from, address _to, uint256 _value)
    notBlacklisted(_msgSender()) notBlacklisted(_from) notBlacklisted(_to)
    internal override(...) {
    if (_to == address(this)) { revert InvalidAccount(); }
    if (!isAfterTradingStartTimestamp()) { ... }

    if (REGISTRY.isLegacyUserAndIsNotActivated(_from) && _msgSender() != owner()) {
        revert AccountNotActivated(_from); // @audit fires for the re-inserted user
    }
    if (REGISTRY.isLegacyUserAndIsNotActivated(_to)) {
        revert AccountNotActivated(_to);
    }
    return super._update(_from, _to, _value);
}
```

Once re-inserted, the user:
1. Cannot transfer their own WLFI (reverts `AccountNotActivated(user)` at line 381).
2. Cannot claim further from the Vester (`VESTER.wlfiClaimFor` internally calls `IERC20(WLFI).safeTransfer(user, claimable)`, which trips the same `_update` check with `_to = user`).
3. Cannot be elected via `WorldLibertyFinancialV3::_electVestingUpdate` (V3 gates on `!REGISTRY.isLegacyUserAndIsNotActivated(_account)`).

The only escape is `WorldLibertyFinancialV2::ownerActivateAccount(user, _bypassVester=true)` — owner must intervene manually to flip `isActivated` back to true without pulling tokens into the Vester (the user cannot be re-pulled because `VESTER.users[user].initialized` is still true from their original activation). Post-recovery the Registry's `amount` no longer matches the Vester's `allocation`, creating a permanent state drift.

**Impact:** The whitelist agent can unilaterally DoS the claims and liquidity of any activated user who has claimed at least 1 wei. Victims lose access to their own WLFI tokens and cannot participate in the V3 election. Scale scales linearly with agent batch size — a single `agentBulkInsertLegacyUsers` call with 500 victim addresses freezes 500 users in one transaction.

An honest agent re-running a batch they previously submitted would unintentionally de-activate any user whose balance has changed since the first run.

**Proof of Concept:** Run the following tests:

```typescript
import { loadFixture } from '@nomicfoundation/hardhat-network-helpers';
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

const IMMEDIATE_TEMPLATE: IWorldLibertyFinancialVester.TemplateStruct = {
  percentageOfAllocation: parseEther('1'),
  startTimestamp: ZERO_BI,
  cliffTimestamp: ZERO_BI,
  endTimestamp: ZERO_BI,
};

describe('WorldLibertyFinancialRegistry — Edge Cases (audit)', () => {
  beforeEach(async () => {
    ctx = await loadFixture(deployWlfiV2Fixture);
  });


  describe('agentBulkInsertLegacyUsers — overwrite activated user (Finding [*`WorldLibertyFinancialRegistry::agentBulkInsertLegacyUsers` can be griefed by dust transfers when WLFI is transferable*](#worldlibertyfinancialregistryagentbulkinsertlegacyusers-can-be-griefed-by-dust-transfers-when-wlfi-is-transferable))', () => {
    it('resets isActivated=false when re-inserting a user who has claimed partial allocation', async function () {
      // activate user normally with cat=1 (retail-like category)
      // Use hhUser2 so initial balance is zero and balance-match check aligns.
      const user = ctx.core.hhUser2;
      const category = 1;

      // Enable cat 1 with immediate-unlock template so user can claim something
      await ctx.vester.connect(ctx.wlfiOwner).ownerSetCategoryEnabled(category, true);
      await ctx.vester.connect(ctx.wlfiOwner).ownerSetCategoryTemplate(category, 0, IMMEDIATE_TEMPLATE);

      await ctx.wlfi.connect(ctx.wlfiOwner).transfer(user.address, DEFAULT_AMOUNT);
      const nonce0 = await ctx.registry.nonce();
      await ctx.registry.connect(ctx.wlfiOwner).agentBulkInsertLegacyUsers(
        nonce0,
        [user.address],
        [DEFAULT_AMOUNT],
        [category],
      );
      await ctx.wlfi.connect(ctx.wlfiOwner).ownerActivateAccount(user.address, false);
      expect(await ctx.registry.isLegacyUserAndIsActivated(user.address)).to.be.true;

      // User claims all their allocation (user now holds 100 WLFI again)
      await advanceTimeToAfterStartTimestamp(ctx);
      await ctx.wlfi.connect(user).claimVest();
      expect(await ctx.wlfi.balanceOf(user.address)).to.eq(DEFAULT_AMOUNT);

      // agent re-inserts the SAME user with their current balance
      const nonce1 = await ctx.registry.nonce();
      await ctx.registry.connect(ctx.wlfiOwner).agentBulkInsertLegacyUsers(
        nonce1,
        [user.address],
        [DEFAULT_AMOUNT],
        [category],
      );

      // isActivated is forcibly reset to false
      expect(await ctx.registry.isLegacyUserAndIsActivated(user.address)).to.be.false;
    });

    it('subsequent transfers from the re-inserted user revert with AccountNotActivated', async function () {
      // Follow-on effect: the V2._update check blocks transfers to/from
      // a legacy-user-not-activated account → user's balance is effectively frozen
      const user = ctx.core.hhUser2;
      const category = 1;

      await ctx.vester.connect(ctx.wlfiOwner).ownerSetCategoryEnabled(category, true);
      await ctx.vester.connect(ctx.wlfiOwner).ownerSetCategoryTemplate(category, 0, IMMEDIATE_TEMPLATE);

      await ctx.wlfi.connect(ctx.wlfiOwner).transfer(user.address, DEFAULT_AMOUNT);
      const nonce0 = await ctx.registry.nonce();
      await ctx.registry.connect(ctx.wlfiOwner).agentBulkInsertLegacyUsers(
        nonce0,
        [user.address],
        [DEFAULT_AMOUNT],
        [category],
      );
      await ctx.wlfi.connect(ctx.wlfiOwner).ownerActivateAccount(user.address, false);
      await advanceTimeToAfterStartTimestamp(ctx);
      await ctx.wlfi.connect(user).claimVest();

      // Re-insert → user is now "legacy-not-activated" again
      const nonce1 = await ctx.registry.nonce();
      await ctx.registry.connect(ctx.wlfiOwner).agentBulkInsertLegacyUsers(
        nonce1,
        [user.address],
        [DEFAULT_AMOUNT],
        [category],
      );

      // User's attempt to transfer their own tokens reverts
      const recipient = ctx.core.hhUser3;
      await expectThrowWithCustomError(
        ctx.wlfi.connect(user).transfer(recipient.address, 1n),
        ctx.wlfi,
        'AccountNotActivated',
        user.address,
      );
    });
  });
});

```

**Recommended Mitigation:** Consider rejecting overwrites of existing entries in `agentBulkInsertLegacyUsers`. This matches the mental model that Registry entries are set once per user at seeding time.

**WLFI:** Fixed in commit [1430e24](https://github.com/worldliberty/usd1-protocol/commit/1430e245349795921bebe275f6bd1d835d9f8fa3).

**Cyfrin:** Verified.

\clearpage
