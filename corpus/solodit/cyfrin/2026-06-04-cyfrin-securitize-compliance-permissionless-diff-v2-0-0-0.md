---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-04-cyfrin-securitize-compliance-permissionless-diff-v2-0-0-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-06-04T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-04-cyfrin-securitize-compliance-permissionless-diff-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-04-cyfrin-securitize-compliance-permissionless-diff-v2-0
title: '`ComplianceServicePermissionless::_lockedAt` and `ComplianceServicePermissionless::_cleanupIssuances`
  perform unguarded `timestamp + lockPeriod` addition, allowing a transfer agent to
  freeze transfers and issuances'
vuln_class: []
---

# `ComplianceServicePermissionless::_lockedAt` and `ComplianceServicePermissionless::_cleanupIssuances` perform unguarded `timestamp + lockPeriod` addition, allowing a transfer agent to freeze transfers and issuances

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-04-cyfrin-securitize-compliance-permissionless-diff-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-04-cyfrin-securitize-compliance-permissionless-diff-v2.0.md)_

---

**Description:** [PR-87](https://github.com/securitize-io/dstoken/pull/87/changes) introduces `ComplianceServicePermissionless` with its own wallet-keyed lockup engine.

Both internal helpers compute `timestamp + lockPeriod` in checked arithmetic, with no upper-bound guard:

```solidity
// contracts/compliance/ComplianceServicePermissionless.sol
function _lockedAt(address _wallet, uint256 _time) internal view returns (uint256) {
    uint256 lockPeriod = getComplianceConfigurationService().getNonUSLockPeriod();
    if (lockPeriod == 0) return 0;
    ...
    for (uint256 i = 0; i < count; i++) {
        if (walletIssuancesTimestamps[_wallet][i] + lockPeriod > _time) { // @audit unchecked addition overflow → panic revert
            totalLockedShares += walletIssuancesValues[_wallet][i];
        }
    }
    ...
}

function _cleanupIssuances(address _wallet) internal {
    uint256 lockPeriod = getComplianceConfigurationService().getNonUSLockPeriod();
    ...
    while (currentIndex < currentCount) {
        if (walletIssuancesTimestamps[_wallet][currentIndex] + lockPeriod <= block.timestamp) { // @audit same issue
            ...
        }
    }
}
```

The same bug class was identified and fixed for `ComplianceServiceRegulated:cleanupInvestorIssuances` **inside this same PR** (commit `337f0ff feature@BC-2118: Fix cleanup_underflow_dos_on_large_lock_period`):

```solidity
// contracts/compliance/ComplianceServiceRegulated.sol - line 902
uint256 time = block.timestamp;

if (lockTime > time) return; // @audit fix added in this PR — NOT ported to permissionless

uint256 currentIssuancesCount = issuancesCounters[investor];
```

The same early-return guard was not applied to the two new permissionless helpers, even though they share the identical arithmetic pattern.

There are two distinct ways to trigger the overflow:

_Variant A — `setNonUSLockPeriod(type(uint256).max)`_
`ComplianceConfigurationService:setNonUSLockPeriod` is `onlyTransferAgentOrAbove`. Setting it to `type(uint256).max` makes every record's `timestamp + lockPeriod` overflow on every call. Every transfer routes through `ComplianceService:validateTransfer → ComplianceServicePermissionless:newPreTransferCheck → _lockedAt` and panics.

Every issuance to any non-platform wallet with at least one prior record routes through `ComplianceService:validateIssuance → ComplianceServicePermissionless:recordIssuance → _cleanupIssuances` and panics. The token becomes fully frozen.

_Variant B — Issuer-supplied `_issuanceTime = type(uint256).max`_
The permissionless override of `ComplianceServicePermissionless:validateIssuanceTime` returns `_issuanceTime` unchanged (it drops the `disallowBackDating` clamp from `ComplianceService:validateIssuanceTime`). An issuer call `dsToken.issueTokensCustom(victim, 1, type(uint256).max, 0, "", 0)` writes `walletIssuancesTimestamps[victim][count] = 2**256 - 1`. Any subsequent `_lockedAt(victim, _)` and `_cleanupIssuances(victim)` panic on that slot — permanently DoSing both transfers from and issuances to `victim`. Unlike Variant A this is per-wallet and cannot be cleared by reading `_cleanupIssuances` (which itself panics on the poisoned record).



**Impact:**
- _Variant A_: Token-wide DoS of all transfers and further issuances. Recovery requires the Transfer Agent to call `setNonUSLockPeriod(0)` or any value such that `(2**256 - 1) - max(timestamps)` does not overflow — feasible but destroys the lockup configuration in the process.

- _Variant B_: permanent per-wallet DoS for the targeted address. `_cleanupIssuances` cannot remove the poisoned record because it itself panics evaluating the slot. The only recovery is `setNonUSLockPeriod(0)` token-wide, which abandons the lockup mechanism — the only on-chain compliance enforcement in the permissionless model.


**Proof of Concept:** Run the following test:

```typescript
import hre from "hardhat";
import { expect } from "chai";
import { loadFixture, time } from "@nomicfoundation/hardhat-toolbox/network-helpers";
import { deployDSTokenPermissionless, DAYS } from "../utils/fixture";
import { DSConstants } from "../../utils/globals";

describe(" setNonUSLockPeriod(type(uint256).max) freezes transfers and issuance", function () {
  const LOCK_PERIOD = 30 * DAYS;

  async function fixtureWithLockupAndIssuance() {
    const contracts = await loadFixture(deployDSTokenPermissionless);
    const { dsToken, trustService, complianceService, complianceConfigurationService } = contracts;

    const [master, transferAgent, user1, user2] = await hre.ethers.getSigners();
    await trustService.connect(master).setRole(transferAgent, DSConstants.roles.TRANSFER_AGENT);

    const user1Address = await user1.getAddress();
    const user2Address = await user2.getAddress();

    await complianceConfigurationService.connect(transferAgent).setNonUSLockPeriod(LOCK_PERIOD);
    await dsToken.issueTokens(user1Address, 1_000);

    return { dsToken, complianceService, complianceConfigurationService, transferAgent, user1, user1Address, user2, user2Address };
  }


  it("setNonUSLockPeriod(type(uint256).max) panics every transfer-path call", async function () {
    const { dsToken, complianceService, complianceConfigurationService, transferAgent, user1, user1Address, user2Address } = await fixtureWithLockupAndIssuance();

    // ATTACK: Transfer Agent sets lockPeriod to type(uint256).max
    await complianceConfigurationService.connect(transferAgent).setNonUSLockPeriod(hre.ethers.MaxUint256);

    // Every transfer-path call now hits `timestamps[i] + lockPeriod` overflow.
    await expect(complianceService.lockedAt(user1Address, await time.latest())).to.be.revertedWithPanic(0x11);
    await expect(complianceService.preTransferCheck(user1Address, user2Address, 1)).to.be.revertedWithPanic(0x11);
    await expect(dsToken.connect(user1).transfer(user2Address, 1)).to.be.revertedWithPanic(0x11);

    // Issuance to a wallet with an existing record routes through _cleanupIssuances → panics too.
    await expect(dsToken.issueTokens(user1Address, 1)).to.be.revertedWithPanic(0x11);
  });

  it("token-wide freeze — every holder is affected", async function () {
    const { dsToken, complianceConfigurationService, transferAgent, user1, user1Address, user2Address } = await fixtureWithLockupAndIssuance();
    await dsToken.issueTokens(user2Address, 500);

    await complianceConfigurationService.connect(transferAgent).setNonUSLockPeriod(hre.ethers.MaxUint256);

    await expect(dsToken.connect(user1).transfer(user2Address, 1)).to.be.revertedWithPanic(0x11);
    const user2 = (await hre.ethers.getSigners())[3];
    await expect(dsToken.connect(user2).transfer(user1Address, 1)).to.be.revertedWithPanic(0x11);
    await expect(dsToken.issueTokens(user1Address, 1)).to.be.revertedWithPanic(0x11);
    await expect(dsToken.issueTokens(user2Address, 1)).to.be.revertedWithPanic(0x11);
  });

  it("recovery requires setNonUSLockPeriod(0), destroying the lockup configuration", async function () {
    const { dsToken, complianceConfigurationService, transferAgent, user1, user1Address, user2Address } = await fixtureWithLockupAndIssuance();

    await complianceConfigurationService.connect(transferAgent).setNonUSLockPeriod(hre.ethers.MaxUint256);
    await expect(dsToken.connect(user1).transfer(user2Address, 1)).to.be.revertedWithPanic(0x11);

    // Only escape: abandon the lockup mechanism entirely.
    await complianceConfigurationService.connect(transferAgent).setNonUSLockPeriod(0);
    await expect(dsToken.connect(user1).transfer(user2Address, 1)).to.not.be.reverted;
    expect(await dsToken.balanceOf(user2Address)).to.equal(1);
  });
});
```
**Recommended Mitigation:** Consider implementing following fix:

```diff
 function _lockedAt(address _wallet, uint256 _time) internal view returns (uint256) {
     uint256 lockPeriod = getComplianceConfigurationService().getNonUSLockPeriod();
     if (lockPeriod == 0) return 0;
+    if (lockPeriod > _time) return 0;

     uint256 count = walletIssuancesCounters[_wallet];
     if (count == 0) return 0;
     ...
 }

 function _cleanupIssuances(address _wallet) internal {
     uint256 lockPeriod = getComplianceConfigurationService().getNonUSLockPeriod();
+    if (lockPeriod > block.timestamp) return;
     uint256 currentCount = walletIssuancesCounters[_wallet];
     ...
 }

 function validateIssuanceTime(uint256 _issuanceTime)
     public view virtual override returns (uint256)
 {
-    return _issuanceTime;
+    return _issuanceTime > block.timestamp ? block.timestamp : _issuanceTime;
 }
```
**Securitize:** Fixed in [a36bb0a](https://github.com/securitize-io/dstoken/commit/a36bb0a55c7c68e6a6402baf66e71a0327e8bb99).

**Cyfrin:**
Verified.
