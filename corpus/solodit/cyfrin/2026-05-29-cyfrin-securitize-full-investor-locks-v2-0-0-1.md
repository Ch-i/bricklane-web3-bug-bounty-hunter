---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-29-cyfrin-securitize-full-investor-locks-v2-0-0-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-05-29T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-29-cyfrin-securitize-full-investor-locks-v2-0
title: '`ComplianceServiceWhitelisted::doPreTransferCheckWhitelisted` missing platform-wallet
  and reallocation carve-outs'
vuln_class: []
---

# `ComplianceServiceWhitelisted::doPreTransferCheckWhitelisted` missing platform-wallet and reallocation carve-outs

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md)_

---

**Description:** BC-1779's spec (`audit-request-dstoken-freeze.pdf`, Functional Requirements) distinguishes three lock-handling carve-outs:

1. **Platform-wallet sender exemption** (req. 2): platform wallets as senders are exempt from all lock checks.
2. **Full-lock gate** (req. 1): blocks every transfer, including same-investor reallocations.
3. **Partial-lock enforcement** (req. 3): blocks standard transfers but exempts same-investor reallocations.

`ComplianceServiceRegulated::doPreTransferCheckRegulated` at `contracts/compliance/ComplianceServiceRegulated.sol:209-223` implements all three by wrapping the lock checks in an outer `!isPlatformWallet(_from)` envelope, an inner unconditional `isInvestorLocked` gate, and an `!isReallocation`-guarded partial-lock check:

```solidity
if (!IDSWalletManager(_services[WALLET_MANAGER]).isPlatformWallet(_from)) {
    (string memory investorFrom, string memory investorTo) =
        IDSRegistryService(_services[REGISTRY_SERVICE]).getInvestors(_from, _to);
    if (!CommonUtils.isEmptyString(investorFrom) &&
        IDSLockManager(_services[LOCK_MANAGER]).isInvestorLocked(investorFrom)) {
        return (16, TOKENS_LOCKED);
    }
    bool isReallocation = !CommonUtils.isEmptyString(investorFrom) &&
        CommonUtils.isEqualString(investorFrom, investorTo);
    if (!isReallocation &&
        IDSLockManager(_services[LOCK_MANAGER]).getTransferableTokens(_from, block.timestamp) < _value) {
        return (16, TOKENS_LOCKED);
    }
}
```

`ComplianceServiceWhitelisted::doPreTransferCheckWhitelisted` at `contracts/compliance/ComplianceServiceWhitelisted.sol:114` collapses all three into a single unconditional check:

```solidity
if (getLockManager().getTransferableTokens(_from, block.timestamp) < _value) {
    return (16, TOKENS_LOCKED);
}
```

Two regressions follow.

**Regression 1 - Platform-wallet sender bricked.** BC-1779 specifically removed the previous `!isPlatformWallet(_from) &&` prefix from this line. Platform wallets have no investor record (`WalletManager::setSpecialWallet` requires `getInvestor(_wallet)` to be empty), so `getInvestor(platformWallet)` returns `""`. `InvestorLockManager::getTransferableTokensForInvestor("", _time)` reads `investorsLocked[""] = false`, computes `balanceOfInvestor("") = 0` (the token library skips writes on empty investor ids), `investorsLocksCounts[""] = 0`, takes the no-locks fast path, and returns 0. The compare `0 < _value` is true for any positive transfer, and the function returns `(16, TOKENS_LOCKED)`. Every platform-wallet-originated transfer reverts.

**Regression 2 - Same-investor reallocation under partial lock bricked.** Without the `isReallocation` predicate, an investor whose entire balance is covered by an active partial lock entry cannot rotate tokens to a different wallet of their own. `InvestorLockManager::addManualLockRecord(wallet, value, reason, releaseTime)` writes the partial-lock entry at the investor level (`investorsLocks[id][i]`). `getTransferableTokensForInvestor(id, time)` then walks `investorsLocks[id][...]`, sums the still-locked balance into `totalLockedTokens`, and returns `balance - totalLocked = 0`. The same `(16, TOKENS_LOCKED)` revert fires. The regulated variant exempts this case via the `!isReallocation` guard; the whitelisted variant has no such guard.

`ComplianceServiceGlobalWhitelisted::preTransferCheck` chains to `super.preTransferCheck`, so both regressions propagate unchanged to global-whitelisted deployments.

A subtle observation about the correct fix shape: adding `!isReallocation &&` to line 114 alone would inadvertently re-introduce a worse bug. The whitelisted variant has no separate full-investor-lock gate; the only place `isInvestorLocked` is enforced is the `if (investorsLocked[id]) return 0` early-return inside `getTransferableTokensForInvestor`. Skipping the line-114 check on reallocations would also skip that early-return, allowing fully-locked investors to reallocate. The structurally correct fix lifts the regulated variant's full multi-guard block (separate full-lock gate + reallocation-guarded partial-lock gate + outer platform-wallet envelope), not just a single predicate.

**Files:**

`ComplianceServiceWhitelisted::doPreTransferCheckWhitelisted`

**Impact:** Both regressions fire on every WHITELISTED / GLOBAL_WHITELISTED deployment - the documented operational pattern uses platform wallets for issuer-side flows (treasury rebalancing, redemption payout, distribution) and supports same-investor wallet rotation as a non-custodial recovery primitive (hot-to-cold migration, multi-sig consolidation, compromised-key recovery, hardware-wallet upgrades). The revert reason (`Tokens Locked`, code 16) misdirects diagnosis toward the lock manager rather than toward the missing carve-outs. No funds are at risk on either path; the impact is operational denial-of-service. Admin recovery requires a code upgrade or, for regression 1, a workaround of de-designating-and-re-designating the platform wallet around each affected transfer (which loses every platform-wallet exemption elsewhere in the regulated machinery during the window). Both bugs are absent on the REGULATED-variant deployment.

**Proof of Concept:** Add the following test to `test/solace-pocs/M-1.test.ts` and run with: `npx hardhat test test/solace-pocs/M-1.test.ts`.

```typescript
// PoC: ComplianceServiceWhitelisted::doPreTransferCheckWhitelisted at line 114
// collapses the three lock-check carve-outs of the regulated variant into a
// single unconditional getTransferableTokens check. Two regressions follow:
//
//   1. Platform-wallet sender carve-out (removed by BC-1779): every
//      platform-wallet-originated transfer reverts because
//      getInvestor(platformWallet) returns "" and getTransferableTokens("")
//      returns 0 via the no-locks fast path, so 0 < _value is always true.
//
//   2. Same-investor reallocation carve-out (never present): every transfer
//      where _from and _to belong to the same investor reverts under any
//      active partial lock, because the reallocation predicate is never
//      computed on the whitelisted path.
//
// The regulated variant's doPreTransferCheckRegulated (lines 209-223) wraps
// the lock lookup in (a) an outer !isPlatformWallet(_from) envelope,
// (b) an unconditional isInvestorLocked gate, and (c) a !isReallocation-guarded
// partial-lock check. The whitelisted variant has none of these guards.

import hre from 'hardhat';
import { expect } from 'chai';
import { loadFixture, time } from '@nomicfoundation/hardhat-toolbox/network-helpers';
import { deployDSTokenWhitelisted, INVESTORS } from '../utils/fixture';
import { registerInvestor } from '../utils/test-helper';

describe('PoC: doPreTransferCheckWhitelisted missing platform-wallet sender and reallocation carve-outs', function () {
  it('regression 1: platform-wallet sender transfer reverts with TOKENS_LOCKED', async function () {
    const [deployer, platformWallet, investorWallet] = await hre.ethers.getSigners();
    const { dsToken, registryService, walletManager } = await loadFixture(deployDSTokenWhitelisted);

    await walletManager.addPlatformWallet(await platformWallet.getAddress());
    await registerInvestor(
      INVESTORS.INVESTOR_ID.INVESTOR_ID_1,
      await investorWallet.getAddress(),
      registryService,
    );
    await dsToken.issueTokens(await platformWallet.getAddress(), 1000n);

    // BUG: platform-wallet egress reverts because getInvestor(platformWallet)
    // returns "", getTransferableTokens("") returns 0, and 0 < _value is true.
    await expect(
      dsToken.connect(platformWallet).transfer(await investorWallet.getAddress(), 100n),
    ).to.be.revertedWith('Tokens Locked');

    // Confirm the revert truly reverted (no partial state mutation).
    expect(await dsToken.balanceOf(await platformWallet.getAddress())).to.equal(1000n);
    expect(await dsToken.balanceOf(await investorWallet.getAddress())).to.equal(0n);
  });

  it('regression 2: same-investor reallocation under partial lock reverts with TOKENS_LOCKED', async function () {
    const [deployer, wallet1, wallet2] = await hre.ethers.getSigners();
    const { dsToken, registryService, lockManager } = await loadFixture(deployDSTokenWhitelisted);

    // Single investor with TWO wallets (wallet1 and wallet2 both resolve to
    // INVESTOR_ID_1).
    await registerInvestor(
      INVESTORS.INVESTOR_ID.INVESTOR_ID_1,
      await wallet1.getAddress(),
      registryService,
    );
    await registryService.addWallet(
      await wallet2.getAddress(),
      INVESTORS.INVESTOR_ID.INVESTOR_ID_1,
    );
    await dsToken.issueTokens(await wallet1.getAddress(), 100n);

    // Active partial lock covering the full balance, release time 1 day out.
    // addManualLockRecord resolves the wallet to its investor and stores the
    // record at the investor level (investorsLocks[INVESTOR_ID_1][0]). The
    // full-investor-lock flag (investorsLocked[INVESTOR_ID_1]) is NOT set.
    await lockManager.addManualLockRecord(
      await wallet1.getAddress(),
      100n,
      'partial lock',
      (await time.latest()) + 24 * 60 * 60,
    );

    // BUG: same-investor reallocation reverts. The whitelisted variant never
    // resolves investorFrom / investorTo and never computes isReallocation.
    // getTransferableTokens(wallet1, ...) sums the full balance into the
    // locked total and returns 0; the unconditional `0 < 100` reverts. The
    // regulated variant exempts this case via the !isReallocation guard
    // around the partial-lock check.
    await expect(
      dsToken.connect(wallet1).transfer(await wallet2.getAddress(), 100n),
    ).to.be.revertedWith('Tokens Locked');

    // Balances unchanged (no partial mutation).
    expect(await dsToken.balanceOf(await wallet1.getAddress())).to.equal(100n);
    expect(await dsToken.balanceOf(await wallet2.getAddress())).to.equal(0n);
  });
});
```

Test result on the unfixed codebase:

```
PoC: doPreTransferCheckWhitelisted missing platform-wallet sender and reallocation carve-outs
  ✔ regression 1: platform-wallet sender transfer reverts with TOKENS_LOCKED
  ✔ regression 2: same-investor reallocation under partial lock reverts with TOKENS_LOCKED

2 passing
```

Both regressions fire against the unfixed whitelisted variant; both pass against the regulated variant (where the three-guard structure handles each case correctly).

**Recommended Mitigation:** Lift the regulated variant's full multi-guard structure into `doPreTransferCheckWhitelisted`. The single patch closes both regressions and brings the whitelisted tier into parity with the regulated tier's spec enforcement. Replace line 114 with:

```solidity
if (!getWalletManager().isPlatformWallet(_from)) {
    (string memory investorFrom, string memory investorTo) =
        getRegistryService().getInvestors(_from, _to);

    // Full investor lock blocks everything including reallocations.
    if (!CommonUtils.isEmptyString(investorFrom) &&
        getLockManager().isInvestorLocked(investorFrom)) {
        return (16, TOKENS_LOCKED);
    }

    // Partial lock skips same-investor reallocations.
    bool isReallocation = !CommonUtils.isEmptyString(investorFrom) &&
        CommonUtils.isEqualString(investorFrom, investorTo);
    if (!isReallocation &&
        getLockManager().getTransferableTokens(_from, block.timestamp) < _value) {
        return (16, TOKENS_LOCKED);
    }
}
```


**Securitize:** Fixed in [da3c9c2](https://github.com/securitize-io/dstoken/commit/da3c9c2aeee9ffdf0f54ce4913c197871eb5454a).

**Cyfrin:** Verified.
