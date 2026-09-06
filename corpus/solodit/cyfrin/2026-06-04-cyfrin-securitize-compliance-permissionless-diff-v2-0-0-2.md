---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-04-cyfrin-securitize-compliance-permissionless-diff-v2-0-0-2
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-06-04T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-04-cyfrin-securitize-compliance-permissionless-diff-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-04-cyfrin-securitize-compliance-permissionless-diff-v2-0
title: '`ComplianceServicePermissionless::recordIssuance` writes a lockup record even
  when the lock period is zero, causing tokens minted with no lockup to be retroactively
  locked when a lockup is later enabled'
vuln_class: []
---

# `ComplianceServicePermissionless::recordIssuance` writes a lockup record even when the lock period is zero, causing tokens minted with no lockup to be retroactively locked when a lockup is later enabled

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-04-cyfrin-securitize-compliance-permissionless-diff-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-04-cyfrin-securitize-compliance-permissionless-diff-v2.0.md)_

---

**Description:** The audit-scope document FR-6 specifies: *"The lockup window is read from `ComplianceConfigurationService.getNonUSLockPeriod()` at evaluation time (not stored per-record). Period = 0 → no lockup enforced **and no lockup record written**."*

`ComplianceServicePermissionless:recordIssuance` does not honor the "no lockup record written" half of FR-6. It unconditionally writes an issuance record for every non-platform recipient, regardless of the configured lock period:

```solidity
// compliance/ComplianceServicePermissionless.sol
function recordIssuance(address _to, uint256 _value, uint256 _issuanceTime)
    internal virtual override returns (bool)
{
    if (getWalletManager().isPlatformWallet(_to)) {
        return true;                               // @audit only platform wallets are exempt
    }

    _cleanupIssuances(_to);
    require(walletIssuancesCounters[_to] < MAX_ISSUANCES_PER_WALLET, "Issuance cap reached");

    uint256 shares = getRebasingProvider().convertTokensToShares(_value);
    uint256 count = walletIssuancesCounters[_to];
    walletIssuancesValues[_to][count] = shares;            // @audit record written
    walletIssuancesTimestamps[_to][count] = _issuanceTime; // @audit even when getNonUSLockPeriod() == 0
    walletIssuancesCounters[_to] = count + 1;

    emit IssuanceRecorded(_to, shares, _issuanceTime);
    return true;
}
```

The danger is that `ComplianceServicePermissionless:_lockedAt` reads the lock period at *evaluation* time, not at *record* time:

```solidity
// compliance/ComplianceServicePermissionless.sol
function _lockedAt(address _wallet, uint256 _time) internal view returns (uint256) {
    uint256 lockPeriod = getComplianceConfigurationService().getNonUSLockPeriod();
    if (lockPeriod == 0) return 0;          // @audit dormant only while the period stays 0
    ...
    for (uint256 i = 0; i < count; i++) {
        if (walletIssuancesTimestamps[_wallet][i] + lockPeriod > _time) { // @audit old period-0 record re-evaluated against the NEW period
            totalLockedShares += walletIssuancesValues[_wallet][i];
        }
    }
    ...
}
```

A record written during a period-0 window is harmless *only while the period remains 0* (because `_lockedAt` short-circuits). The instant a non-zero lock period is configured, every such record whose original `_issuanceTime` is within `lockPeriod` seconds of "now" is treated as locked — retroactively freezing tokens that were minted as freely transferable.

Note that the period-0 case IS handled in `_lockedAt` (early return) and in `_cleanupIssuances` (records sweep when `timestamp + 0 <= block.timestamp`), but it is NOT handled in `recordIssuance`, which is exactly where FR-6 places the responsibility.

Consider following sequence:

```text
1. Issuer mints 1000 to user1 while getNonUSLockPeriod() == 0 (the deployment default).
     → walletIssuancesTimestamps[user1][0] = T1, walletIssuancesCounters[user1] = 1
     → transfers work, because _lockedAt short-circuits on lockPeriod == 0
2. user1 treats the 1000 tokens as freely transferable (they were minted with no lockup).
3. Transfer Agent later enables a 30-day lockup for go-forward issuances:
     setNonUSLockPeriod(30 days)
4. user1 attempts to transfer → _lockedAt(user1, now) now sees lockPeriod = 30d,
     evaluates T1 + 30d > now → true → 1000 locked → transfer reverts with code 16.
5. The lock persists until T1 + 30 days — anchored to the ORIGINAL mint time, not to
     the policy-change time.
```



**Impact:** When a Transfer Agent enables a lockup, every holder who received a period-0 mint within the trailing `lockPeriod` window is simultaneously and unexpectedly frozen — a transfer DoS for up to `lockPeriod` from each mint's original timestamp.

It is noted that there is no permanent loss (the lock expires at `mintTime + lockPeriod`), but holders who acquired or planned around the freely-transferable status are blocked for a bounded but potentially long window.


**Proof of Concept:** Run the following test:

```typescript
import hre from "hardhat";
import { expect } from "chai";
import { loadFixture, time } from "@nomicfoundation/hardhat-toolbox/network-helpers";
import { deployDSTokenPermissionless, DAYS } from "../utils/fixture";
import { DSConstants } from "../../utils/globals";

describe("PoC M-02 — period-0 mint creates a record that a later lockup retroactively locks", function () {
  async function fixture() {
    const contracts = await loadFixture(deployDSTokenPermissionless);
    const { dsToken, trustService, complianceService, complianceConfigurationService } = contracts;
    const [master, transferAgent, user1, user2] = await hre.ethers.getSigners();
    await trustService.connect(master).setRole(transferAgent, DSConstants.roles.TRANSFER_AGENT);
    return {
      dsToken,
      complianceService,
      complianceConfigurationService,
      transferAgent,
      user1,
      user2,
      user1Address: await user1.getAddress(),
      user2Address: await user2.getAddress(),
    };
  }

  it("PoC: mint at lockPeriod==0 records an issuance despite FR-6", async function () {
    const { dsToken, complianceService, complianceConfigurationService, user1Address } = await fixture();

    expect(await complianceConfigurationService.getNonUSLockPeriod()).to.equal(0);

    await dsToken.issueTokens(user1Address, 1_000);

    // FR-6 says NO record should be written at period 0 — but one is.
    expect(await complianceService.issuancesCount(user1Address)).to.equal(1);

    // At period 0 the token is still transferable (lockedAt short-circuits on lockPeriod==0)
    const now = await time.latest();
    expect(await complianceService.lockedAt(user1Address, now + 1)).to.equal(0);
  });

  it("PoC: enabling a lockup later retroactively locks the period-0 mint", async function () {
    const { dsToken, complianceService, complianceConfigurationService, transferAgent, user1, user1Address, user2Address } = await fixture();

    // 1. Mint 1000 while there is NO lockup. Holder reasonably expects free transfer forever.
    await dsToken.issueTokens(user1Address, 1_000);

    let check = await complianceService.preTransferCheck(user1Address, user2Address, 1_000);
    expect(check[0]).to.equal(0n); // VALID

    // 2. One day later the Transfer Agent enables a 30-day lockup (for go-forward issuances).
    await time.increase(1 * DAYS);
    await complianceConfigurationService.connect(transferAgent).setNonUSLockPeriod(30 * DAYS);

    // 3. The OLD mint is now retroactively locked, even though it predates the lockup.
    check = await complianceService.preTransferCheck(user1Address, user2Address, 1_000);
    expect(check[0]).to.equal(16n); // TOKENS_LOCKED
    expect(check[1]).to.equal("Tokens Locked");
    await expect(dsToken.connect(user1).transfer(user2Address, 1_000)).to.be.reverted;

    // lockedAt reports the full balance as locked, anchored to the ORIGINAL mint time
    const now = await time.latest();
    expect(await complianceService.lockedAt(user1Address, now)).to.equal(1_000);

    // 4. The lock persists until 30 days after the ORIGINAL issuance, not the policy change.
    await time.increase(29 * DAYS);
    check = await complianceService.preTransferCheck(user1Address, user2Address, 1_000);
    expect(check[0]).to.equal(0n); // VALID again once original-mint + 30d elapses
  });
});
```

**Recommended Mitigation:** Consider following fix:

```diff
 function recordIssuance(address _to, uint256 _value, uint256 _issuanceTime)
     internal virtual override returns (bool)
 {
     if (getWalletManager().isPlatformWallet(_to)) {
         return true;
     }

+    if (getComplianceConfigurationService().getNonUSLockPeriod() == 0) {
+        return true;
+    }

     _cleanupIssuances(_to);

    ...
 }
```
**Securitize:** Fixed in [f6f44f6](https://github.com/securitize-io/dstoken/commit/f6f44f6c3b00cf7071b7e8abea29da9c271ad34a).

**Cyfrin:**
Verified.

\clearpage
