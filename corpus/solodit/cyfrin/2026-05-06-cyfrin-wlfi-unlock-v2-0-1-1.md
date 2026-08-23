---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-06-cyfrin-wlfi-unlock-v2-0-1-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-05-06T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-06-cyfrin-wlfi-unlock-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-06-cyfrin-wlfi-unlock-v2-0
title: '`WorldLibertyFinancialV3::_electVestingUpdate` does not verify `Vester` initialization,
  letting owner skip the 10% burn'
vuln_class: []
---

# `WorldLibertyFinancialV3::_electVestingUpdate` does not verify `Vester` initialization, letting owner skip the 10% burn

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-06-cyfrin-wlfi-unlock-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-06-cyfrin-wlfi-unlock-v2.0.md)_

---

**Description:** `WorldLibertyFinancialV3::_electVestingUpdate` determines the 10% burn amount by reading `VESTER.allocation(_account)`. If the Vester has no record for the user, that view returns `0`, so the computed burn amount is `0 / 10 = 0`.

Both `VESTER.wlfiBurnAllocation` and `REGISTRY.wlfiBurnAllocation` then no-op silently (no `initialized` check on Vester's side), and `wlfiSetCategory` flips the category to 47 on both contracts without any token movement.

This "no Vester record despite Registry activation" state is reachable through the `_bypassVester=true` branch in V2's `_activateAccount`:

```solidity
// WorldLibertyFinancialV2.sol
function _activateAccount(address _account, bool _bypassVester) internal {
    REGISTRY.wlfiActivateAccount(_account);
    uint8 category = REGISTRY.getLegacyUserCategory(_account);
    uint112 allocation = REGISTRY.getLegacyUserAllocation(_account);

    if (!_bypassVester) { // @audit when true, skips Vester.wlfiActivateVest
        _approve(_account, address(VESTER), 0);
        _approve(_account, address(VESTER), allocation);
        VESTER.wlfiActivateVest(_account, category, allocation);
        assert(allowance(_account, address(VESTER)) == 0);
    }
}
```
`WorldLibertyFinancialV3::_electVestingUpdate` then trusts Registry's `isActivated = true` and proceeds even though Vester state is empty:

```solidity
// WorldLibertyFinancialV3.sol
function _electVestingUpdate(address _account) internal {
    if (!REGISTRY.isLegacyUser(_account)) {
        revert InvalidAccount();
    }
    if (REGISTRY.isLegacyUserAndIsNotActivated(_account)) { // @audit only checks Registry, not Vester
        revert AccountNotActivated(_account);
    }
    ...
    if (newCategory == 47) {
        uint256 allocation = VESTER.allocation(_account); // @audit returns 0 for non-initialized users
        uint256 amountToBurn = allocation / 10;            // @audit 0 / 10 = 0
        VESTER.wlfiBurnAllocation(_account, amountToBurn); // @audit no-op with _amount = 0
        REGISTRY.wlfiBurnAllocation(_account, amountToBurn); // @audit no-op with _amount = 0
    }
    VESTER.wlfiSetCategory(_account, newCategory); // @audit writes cat=47 on uninitialized Vester record
    REGISTRY.wlfiSetCategory(_account, newCategory);
    ...
}
```
`WorldLibertyFinancialVester::wlfiBurnAllocation` and `wlfiSetCategory` each omit an `initialized` check, completing the silent-no-op path:

```solidity
// WorldLibertyFinancialVester.sol
function wlfiBurnAllocation(address _user, uint256 _amount) external whenNotPaused {
    if (msg.sender != address(WLFI)) { revert Unauthorized(); }
    VesterStorage storage $ = _getStorage();
    UserInfo storage userInfo = $.users[_user];
    userInfo.allocation -= uint112(_amount); // @audit 0 - 0 = 0 no-op
    assert(userInfo.claimed <= userInfo.allocation);
    ...
}

function wlfiSetCategory(address _user, uint8 _category) external whenNotPaused {
    if (msg.sender != address(WLFI)) { revert Unauthorized(); }
    VesterStorage storage $ = _getStorage();
    if (!$.categoryInfo[_category].enabled) { revert CategoryNotEnabled(_category); }
    UserInfo storage userInfo = $.users[_user];
    // @audit no `initialized` check — writes category on empty record
    uint8 oldCategory = userInfo.category;
    userInfo.category = _category;
    ...
}
```

Attack flow:
1. Owner calls `V2.ownerActivateAccount(teamUser, true)` — Registry flips `isActivated=true`; Vester remains untouched (no record, no token pull).
2. Owner calls `V3.ownerElectVestingUpdatesFor([teamUser])`. V3 reads `VESTER.allocation(teamUser) = 0`, computes `amountToBurn = 0`, "burns" zero, and flips category to 47 on both contracts.
3. `teamUser` now holds 100% of their WLFI as a fully-liquid balance (Vester has no custody), Registry marks them as cat-47 "elected". **Zero WLFI was burned.**
4. Any attempt to subsequently call `V2.ownerActivateAccount(teamUser, false)` reverts with `AlreadyInitialized` (Registry's `isActivated` already flipped at step 1), so the user CANNOT be pulled into the Vester afterwards. The state is "one-way": team user retains 100% liquid.

**Impact:** Strictly worse than a normal team election. A normal team user pays 10% burn and receives 90% linearly vested over 3 years (Vester custody). A "bypass" team user pays 0% burn and retains 100% fully liquid immediately. For the `teamSigner` reference in the V3 deploy script (`3_750_000_000e18` allocation), this turns a `0.375e27` burn into `0` and lets the user transfer `3.75e27` WLFI immediately instead of waiting 3 years.

**Proof of Concept:** Run the following test:

```typescript
import { loadFixture } from '@nomicfoundation/hardhat-network-helpers';
import { expect } from 'chai';
import { parseEther, TypedDataDomain } from 'ethers';
import hardhat from 'hardhat';
import { deployWlfiV3Fixture } from '../fixtures';
import { expectThrowWithCustomError } from '../utils';
import { advanceTimeToAfterStartTimestamp, signWlfiActivationMessage } from '../wlfi/wlfi-utils';

type Ctx = Awaited<ReturnType<typeof deployWlfiV3Fixture>>;
let ctx: Ctx;


async function insertAndFund(user: { address: string }, amount: bigint, category: number) {
  await ctx.wlfi.connect(ctx.wlfiOwner).transfer(user.address, amount);
  const nonce = await ctx.registry.nonce();
  await ctx.registry.connect(ctx.wlfiOwner).agentBulkInsertLegacyUsers(
    nonce,
    [user.address],
    [amount],
    [category],
  );
}

describe('WorldLibertyFinancialV3 — Edge Cases (audit)', () => {
  beforeEach(async () => {
    ctx = await loadFixture(deployWlfiV3Fixture);

    // Enable categories used across tests (1, 2 for pre-election; 45, 47 for post-election)
    await ctx.vester.connect(ctx.wlfiOwner).ownerSetCategoryEnabled(1, true);
    await ctx.vester.connect(ctx.wlfiOwner).ownerSetCategoryEnabled(2, true);
    await ctx.vester.connect(ctx.wlfiOwner).ownerSetCategoryEnabled(45, true);
    await ctx.vester.connect(ctx.wlfiOwner).ownerSetCategoryEnabled(47, true);

    await advanceTimeToAfterStartTimestamp(ctx);
  });


  describe('bypass-vester', () => {
    it('elects a team user into cat 47 with zero burn when owner uses ownerActivateAccount(user, bypassVester=true)', async function () {
      // team user (cat 2) registered with 100 WLFI; no Vester activation
      const user = ctx.core.hhUser2;
      const amount = parseEther('100');
      await insertAndFund(user, amount, 2);

      const userBalanceBefore = await ctx.wlfi.balanceOf(user.address);
      const vesterBalanceBefore = await ctx.wlfi.balanceOf(ctx.vester);
      const totalSupplyBefore = await ctx.wlfi.totalSupply();

      // Owner calls the bypass-vester activation path: Registry.isActivated flips to true,
      // Vester is NEVER initialized, Vester.allocation(user) remains 0.
      await ctx.wlfi.connect(ctx.wlfiOwner).ownerActivateAccount(user.address, true);

      // owner elects this bypass-activated user
      await ctx.wlfi.connect(ctx.wlfiOwner).ownerElectVestingUpdatesFor([user.address]);

      //no tokens moved, no burn occurred
      expect(await ctx.wlfi.balanceOf(user.address), 'user WLFI balance').to.eq(userBalanceBefore);
      expect(await ctx.wlfi.balanceOf(ctx.vester), 'Vester WLFI balance').to.eq(vesterBalanceBefore);
      expect(await ctx.wlfi.totalSupply(), 'WLFI total supply').to.eq(totalSupplyBefore);

      // Vester has no record (allocation stayed 0), but category was set to 47
      expect(await ctx.vester.allocation(user.address), 'Vester.allocation').to.eq(0n);
      expect(await ctx.vester.unclaimed(user.address), 'Vester.unclaimed').to.eq(0n);

      // Registry reports cat 47 and amount UNCHANGED (since burn amount was 0)
      expect(await ctx.registry.getLegacyUserCategory(user.address), 'Registry cat').to.eq(47);
      expect(await ctx.registry.getLegacyUserAllocation(user.address), 'Registry amount').to.eq(amount);

      // user can still freely transfer WLFI (not a legacy-not-activated user)
      const sink = ctx.core.hhUser3;
      const transferTx = ctx.wlfi.connect(user).transfer(sink.address, amount);
      await expect(transferTx).to.not.be.reverted;
      expect(await ctx.wlfi.balanceOf(sink.address)).to.eq(amount);
    });
  });


});

```

**Recommended Mitigation:** Consider adding a Vester-state check at the top of `_electVestingUpdate`:

```diff
function _electVestingUpdate(address _account) internal {
    if (!REGISTRY.isLegacyUser(_account)) { revert InvalidAccount(); }
    if (REGISTRY.isLegacyUserAndIsNotActivated(_account)) { revert AccountNotActivated(_account); }

++    if (VESTER.allocation(_account) == 0) { revert VesterNotInitialized(_account); }

    ...
}
```

**WLFI:** Fixed in commit [1430e24](https://github.com/worldliberty/usd1-protocol/commit/1430e245349795921bebe275f6bd1d835d9f8fa3).

**Cyfrin:** Verified.
