---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-04-cyfrin-securitize-compliance-permissionless-diff-v2-0-0-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-06-04T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-04-cyfrin-securitize-compliance-permissionless-diff-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-04-cyfrin-securitize-compliance-permissionless-diff-v2-0
title: '`TokenLibrary::issueTokensCustom` routes every manual lock under permissionless
  into a single shared `investorsLocks[""]` bucket, exhausting the global 30-lock
  cap and DoS-ing all future issuances with manual locks'
vuln_class: []
---

# `TokenLibrary::issueTokensCustom` routes every manual lock under permissionless into a single shared `investorsLocks[""]` bucket, exhausting the global 30-lock cap and DoS-ing all future issuances with manual locks

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-04-cyfrin-securitize-compliance-permissionless-diff-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-04-cyfrin-securitize-compliance-permissionless-diff-v2.0.md)_

---

**Description:** [PR-87's](https://github.com/securitize-io/dstoken/pull/87/changes) design premise is that the `!CommonUtils.isEmptyString(investor)` guard at `DSToken:296` and `TokenLibrary:160` makes every investor-keyed bookkeeping path a no-op under `StubRegistryService` (whose `getInvestor(addr)` always returns `""`).

The audit-scope document (FR-1) makes this explicit: *"`tokenData.investorsBalances` must never be written under this configuration."*

That guard exists for `investorsBalances`. It does **not** exist for `InvestorLockManager.investorsLocks`. The manual-lock write path is unconditional:

```solidity
// token/TokenLibrary.sol — issueTokensCustom
function issueTokensCustom(...) public returns (uint256) {
    ...
    IDSComplianceService(_services[COMPLIANCE_SERVICE]).validateIssuance(_params._to, _params._value, _params._issuanceTime);
    ...
    for (uint256 i = 0; i < _params._valuesLocked.length; i++) {
        totalLocked += _params._valuesLocked[i];
        _lockManager.addManualLockRecord(_params._to, _params._valuesLocked[i], _params._reason, _params._releaseTimes[i]); // @audit no dead-branch guard here
    }
    ...
}
```

```solidity
// compliance/InvestorLockManager.sol
function addManualLockRecord(address _to, uint256 _valueLocked, string calldata _reason, uint256 _releaseTime) public override onlyTransferAgentOrAboveOrToken {
    require(_to != address(0), "Invalid address");
    createLock(_to, _valueLocked, 0, _reason, _releaseTime);
}

function createLock(address _to, uint256 _valueLocked, ...) internal {
    createLockForInvestor(getRegistryService().getInvestor(_to), _valueLocked, _reasonCode, _reasonString, _releaseTime); // @audit getInvestor(_to) returns "" under stub — every wallet's lock lands under the SAME key
    ...
}

function createLockForInvestor(string memory _investor, uint256 _valueLocked, ...) public override validLock(...) onlyTransferAgentOrAboveOrToken {
    uint256 totalLockCount = investorsLocksCounts[_investor];
    require(totalLockCount < MAX_LOCKS_PER_INVESTOR, "Too many locks for this investor"); // @audit MAX_LOCKS_PER_INVESTOR = 30, applied to investorId="" globally under stub
    setLockInfoImpl(_investor, totalLockCount, _valueLocked, _reasonCode, _reasonString, _releaseTime);
    ...
}
```

Compare this with the analogous guard that the diff DOES enforce on `investorsBalances`:
```solidity
// token/TokenLibrary.sol — updateInvestorBalance
function updateInvestorBalance(TokenData storage _tokenData, IDSRegistryService _registryService, address _wallet, uint256 _shares, CommonUtils.IncDec _increase) internal {
    string memory investor = _registryService.getInvestor(_wallet);
    if (!CommonUtils.isEmptyString(investor)) { // @audit dead-branch guard present here
        ...
        _tokenData.investorsBalances[investor] = balance;
    }
}
```

Under the stub:
1. `DSToken.issueTokensCustom(to, value, t, _valueLocked > 0, reason, releaseTime)` (or `issueTokensWithMultipleLocks` with a non-empty `_valuesLocked`, or `TokenIssuer.issueTokens` with non-empty `_locksValues`, or `BulkOperator.bulkRegisterAndIssuance` with non-empty entry `locksValues`) — all `onlyIssuerOrAbove`.
2. Reaches `TokenLibrary.issueTokensCustom`'s loop at line 93-96, calls `addManualLockRecord` for each entry.
3. `createLock(_to, ...)` calls `getRegistryService().getInvestor(_to)` — the stub returns `""`.
4. `createLockForInvestor("", _valueLocked, ...)` writes to `investorsLocks[""][count]` and increments `investorsLocksCounts[""]`.
5. After 30 such writes — across ANY combination of wallets — `require(totalLockCount < MAX_LOCKS_PER_INVESTOR)` at `InvestorLockManager:52` reverts, propagating up through the loop and reverting the entire `issueTokens*` transaction.


**Impact:**
- After 30 cumulative issuances-with-locks across the entire token, `Issuer` is locked out of the entire issuance-with-locks workflow. The DoS is silent: the operator sees "Too many locks for this investor" — a confusing error mentioning an investor concept that the permissionless model is supposed to have eliminated. Recovery requires the Transfer Agent to manually call `InvestorLockManager.removeLockRecordForInvestor("", index)` repeatedly to free slots.

- `InvestorLockManager.lockCount(addr)`, `lockInfo(addr, idx)`, and `getTransferableTokens(addr, t)` all key off `getInvestor(addr)`. Under the stub they all return data from `investorsLocks[""]`. Any caller — operator dashboard, off-chain reconciliation, future contract integration — that asks "how many locks does wallet X have?" gets the GLOBAL count regardless of `X`.

**Proof of Concept:** Run the following test:

```typescript
import hre from "hardhat";
import { expect } from "chai";
import { loadFixture, time } from "@nomicfoundation/hardhat-toolbox/network-helpers";
import { deployDSTokenPermissionless, DAYS } from "../utils/fixture";

describe("PoC M-01 — Issuance with locks pollutes shared investorsLocks[\"\"] bucket and exhausts global cap", function () {
  async function permissionlessFixture() {
    const contracts = await loadFixture(deployDSTokenPermissionless);
    const { dsToken, lockManager } = contracts;
    const [master, user1, user2, user3] = await hre.ethers.getSigners();
    return {
      dsToken, lockManager, master, user1, user2, user3,
      user1Address: await user1.getAddress(),
      user2Address: await user2.getAddress(),
      user3Address: await user3.getAddress(),
    };
  }

  it("PoC: a single issuance with `_valueLocked > 0` writes to investorsLocks[\"\"]", async function () {
    const { dsToken, lockManager, user1Address } = await permissionlessFixture();
    expect(await lockManager.lockCountForInvestor("")).to.equal(0);
    const releaseTime = (await time.latest()) + 30 * DAYS;
    await dsToken.issueTokensCustom(user1Address, 50, await time.latest(), 1, "lock-1", releaseTime);
    expect(await lockManager.lockCountForInvestor("")).to.equal(1);
  });

  it("PoC: locks from DIFFERENT wallets all collapse into the same investorsLocks[\"\"] bucket", async function () {
    const { dsToken, lockManager, user1Address, user2Address, user3Address } = await permissionlessFixture();
    const releaseTime = (await time.latest()) + 30 * DAYS;
    await dsToken.issueTokensCustom(user1Address, 50, await time.latest(), 1, "lock-u1", releaseTime);
    await dsToken.issueTokensCustom(user2Address, 50, await time.latest(), 2, "lock-u2", releaseTime);
    await dsToken.issueTokensCustom(user3Address, 50, await time.latest(), 3, "lock-u3", releaseTime);

    expect(await lockManager.lockCountForInvestor("")).to.equal(3);

    // Cross-wallet leakage: per-address queries all return the SAME shared value
    expect(await lockManager.lockCount(user1Address)).to.equal(3);
    expect(await lockManager.lockCount(user2Address)).to.equal(3);
    expect(await lockManager.lockCount(user3Address)).to.equal(3);
  });

  it("PoC: 30 issuances-with-locks exhaust the shared cap, DoS-ing further issuances globally", async function () {
    const { dsToken, lockManager } = await permissionlessFixture();
    const signers = await hre.ethers.getSigners();
    const releaseTime = (await time.latest()) + 30 * DAYS;

    // 30 issuances, round-robin across wallets — no individual wallet receives many locks.
    for (let i = 0; i < 30; i++) {
      const recipient = await signers[(i % 10) + 1].getAddress();
      await dsToken.issueTokensCustom(recipient, 10, await time.latest(), 1, `lock-${i}`, releaseTime);
    }
    expect(await lockManager.lockCountForInvestor("")).to.equal(30);

    // 31st issuance to a fresh wallet reverts at addManualLockRecord even though that
    // wallet has zero individual locks. The cap is global because the bucket is shared.
    const freshRecipient = await signers[15].getAddress();
    await expect(
      dsToken.issueTokensCustom(freshRecipient, 10, await time.latest(), 1, "lock-31", releaseTime)
    ).to.be.revertedWith("Too many locks for this investor");

    // Issuance without a manual lock continues to work — only the locked-issuance workflow is DoS-ed.
    await expect(dsToken.issueTokens(freshRecipient, 10)).to.not.be.reverted;
  });
});
```

**Recommended Mitigation:** Consider adding following fix:

```diff
 // compliance/InvestorLockManager.sol
 function createLockForInvestor(string memory _investor, uint256 _valueLocked, uint256 _reasonCode, string calldata _reasonString, uint256 _releaseTime)
     public
     override
     validLock(_valueLocked, _releaseTime)
     onlyTransferAgentOrAboveOrToken
 {
+    require(!CommonUtils.isEmptyString(_investor), "Empty investor ID");
     uint256 totalLockCount = investorsLocksCounts[_investor];
     require(totalLockCount < MAX_LOCKS_PER_INVESTOR, "Too many locks for this investor");
     setLockInfoImpl(_investor, totalLockCount, _valueLocked, _reasonCode, _reasonString, _releaseTime);
     ...
 }
```
**Securitize:** Fixed in [4b689f6](https://github.com/securitize-io/dstoken/commit/4b689f6320a3c8c13731c82d93517398bad48aa8).

**Cyfrin:**
 Verified.
