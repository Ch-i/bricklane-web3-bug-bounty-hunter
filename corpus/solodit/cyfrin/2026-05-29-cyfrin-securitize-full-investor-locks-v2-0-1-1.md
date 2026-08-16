---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-29-cyfrin-securitize-full-investor-locks-v2-0-1-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-05-29T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-29-cyfrin-securitize-full-investor-locks-v2-0
title: '`ComplianceServiceRegulated::getComplianceTransferableTokens` lockup is current-country-derived,
  shifts on `setCountry`'
vuln_class: []
---

# `ComplianceServiceRegulated::getComplianceTransferableTokens` lockup is current-country-derived, shifts on `setCountry`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md)_

---

**Description:** `ComplianceServiceRegulated::getComplianceTransferableTokens` at `contracts/compliance/ComplianceServiceRegulated.sol:792-824` walks per-issuance lock records and decides which are still locked against a `_lockTime` parameter:

```solidity
for (uint256 i = 0; i < investorIssuancesCount; i++) {
    uint256 issuanceTimestamp = issuancesTimestamps[investor][i];
    if (uint256(_lockTime) > _time || issuanceTimestamp > (_time - uint256(_lockTime))) {
        uint256 tokens = getRebasingProvider().convertSharesToTokens(issuancesValues[investor][i]);
        totalLockedTokens = totalLockedTokens + tokens;
    }
}
```

The `_lockTime` is supplied by the caller; `ComplianceServiceLibrary::checkHoldUp` (lines 134-154) selects between US and non-US lock periods based on the investor's CURRENT country region:

```solidity
if (_isUSLockPeriod) {
    lockPeriod = IDSComplianceConfigurationService(_services[COMPLIANCE_CONFIGURATION_SERVICE]).getUSLockPeriod();
} else {
    lockPeriod = IDSComplianceConfigurationService(_services[COMPLIANCE_CONFIGURATION_SERVICE]).getNonUSLockPeriod();
}
return complianceService.getComplianceTransferableTokens(_from, block.timestamp, uint64(lockPeriod)) < _value;
```

The issuance records themselves (`issuancesTimestamps[investor][i]`, `issuancesValues[investor][i]`) store only the timestamp and share amount. They do NOT store the lock period or the country at the time of issuance.

`RegistryService::setCountry` (lines 113-123) mutates `investors[_id].country` and (via `adjustInvestorCountsAfterCountryChange`) reconciles the regional counters, but does NOT mutate the per-issuance lock records. The applicable lockup window therefore shifts retroactively after a country change. Two failure modes follow:

1. Lockup shortening: a US investor with active issuance records subject to a longer US lockup is re-countried to a non-US country with a shorter `nonUSLockPeriod`. The next `checkHoldUp` call evaluates those records against the shorter lockup, freeing tokens earlier than the regulatory rule the lockup encodes.

2. Lockup voiding: if the new country resolves to NONE (region 0), the non-US lock period applies; depending on the configured `nonUSLockPeriod` value and the record age, records that should still be locked under US semantics may be evaluated as expired immediately. A related destructive path exists through `cleanupInvestorIssuances`, which also reads the current country and permanently deletes records that the shortened lockup evaluates as expired; the read-path bug here applies independently and reversibly to live lockup checks even when no cleanup runs.

**Files:**

`ComplianceServiceRegulated::getComplianceTransferableTokens`, `ComplianceServiceRegulated::createIssuanceInformation`, `ComplianceServiceLibrary::checkHoldUp`

**Impact:** Concrete reproduction of the US-to-non-US shortening case:

- `getUSLockPeriod() = 365 days`, `getNonUSLockPeriod() = 90 days`.
- Day 0: investor `X` in country `US`, master issues 1000 tokens to walletX via `DSToken::issueTokens(walletX, 1000, t0)`. `issuancesTimestamps["X"][0] = t0`, `issuancesValues["X"][0] = 1000 shares`.
- Day 100: walletX attempts `DSToken::transfer(walletExternal, 1000)`. `checkHoldUp` selects `USLockPeriod = 365`; `getComplianceTransferableTokens` evaluates `issuanceTimestamp > (t0 + 100 - 365)` = `t0 > t0 - 265` = true and 1000 tokens still locked. Transfer reverts with HOLD_UP. Correct.
- Day 100: EXCHANGE calls `RegistryService::setCountry("X", "AE")` (UAE, configured as non-US in `countriesCompliances`). `adjustInvestorCountsAfterCountryChange` reconciles `usInvestorsCount` and writes `investors["X"].country = "AE"`. No issuance record is mutated.
- Day 100, immediately after: walletX retries `DSToken::transfer(walletExternal, 1000)`. `checkHoldUp` now selects `NonUSLockPeriod = 90`; `getComplianceTransferableTokens` evaluates `issuanceTimestamp > (t0 + 100 - 90)` = `t0 > t0 + 10` = false and 0 locked. Transfer proceeds.



**Recommended Mitigation:** Snapshot the applicable lock duration at issuance time. Extend `createIssuanceInformation` to write a third field `issuancesLockPeriods[investor][issuanceId]` derived from the investor's country region at that moment, and have `cleanupInvestorIssuances` and `getComplianceTransferableTokens` read this snapshot instead of re-deriving from current country.

```solidity
mapping(string => mapping(uint256 => uint256)) issuancesLockPeriods;

function createIssuanceInformation(string memory _investor, uint256 _shares, uint256 _issuanceTime) internal returns (bool) {
    uint256 issuancesCount = issuancesCounters[_investor];
    issuancesValues[_investor][issuancesCount] = _shares;
    issuancesTimestamps[_investor][issuancesCount] = _issuanceTime;

    string memory country = getRegistryService().getCountry(_investor);
    uint256 region = getComplianceConfigurationService().getCountryCompliance(country);
    uint256 lockPeriod = region == ComplianceServiceLibrary.US
        ? getComplianceConfigurationService().getUSLockPeriod()
        : getComplianceConfigurationService().getNonUSLockPeriod();
    issuancesLockPeriods[_investor][issuancesCount] = lockPeriod;

    issuancesCounters[_investor] = issuancesCount + 1;
    return true;
}
```

`getComplianceTransferableTokens` then ignores its `_lockTime` parameter (or uses it only as a sanity floor) and reads the per-record `issuancesLockPeriods[investor][i]`. `cleanupInvestorIssuances` does the same. The lockup semantics become country-change-immune.

Alternative (one-line, less precise) fix: in both consumers, take the MAX of `(USLockPeriod, NonUSLockPeriod)`. This preserves the strictest lock but applies it uniformly regardless of issuance-time country; non-US issuances then over-lock for the difference between the two periods. The snapshot approach is preferred because it preserves per-region semantics.

**Securitize:** Acknowledged.
