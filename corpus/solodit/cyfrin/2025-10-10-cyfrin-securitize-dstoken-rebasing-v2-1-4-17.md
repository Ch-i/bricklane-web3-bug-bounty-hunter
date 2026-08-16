---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-4-17
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: Don't write to the same storage slot multiple times
vuln_class: []
---

# Don't write to the same storage slot multiple times

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** In EVM writing to storage is expensive; ideally only write to the same storage slot once. For example `ComplianceServiceRegulated::cleanupInvestorIssuances` does this:
```solidity
        uint256 time = block.timestamp;

        uint256 currentIssuancesCount = issuancesCounters[investor];
        uint256 currentIndex = 0;

        if (currentIssuancesCount == 0) {
            return;
        }

        while (currentIndex < currentIssuancesCount) {
            uint256 issuanceTimestamp = issuancesTimestamps[investor][currentIndex];

            bool isNoLongerLocked = issuanceTimestamp <= (time - lockTime);

            if (isNoLongerLocked) {
                if (currentIndex != currentIssuancesCount - 1) {
                    issuancesTimestamps[investor][currentIndex] = issuancesTimestamps[investor][currentIssuancesCount - 1];
                    issuancesValues[investor][currentIndex] = issuancesValues[investor][currentIssuancesCount - 1];
                }

                delete issuancesTimestamps[investor][currentIssuancesCount - 1];
                delete issuancesValues[investor][currentIssuancesCount - 1];

                // @audit storage write to decrement
                issuancesCounters[investor]--;
                // @audit storage read of value just written
                currentIssuancesCount = issuancesCounters[investor];
            } else {
                currentIndex++;
            }
        }
```

This is very inefficient as it results in an additional storage write and storage read during every loop iteration when `isNoLongerLocked == true`. Instead just decrement the `currentIssuancesCount` variable then write once to `issuancesCounters[investor]` after the loop:
```solidity
        while (currentIndex < currentIssuancesCount) {
            uint256 issuanceTimestamp = issuancesTimestamps[investor][currentIndex];

            bool isNoLongerLocked = issuanceTimestamp <= (time - lockTime);

            if (isNoLongerLocked) {
                if (currentIndex != currentIssuancesCount - 1) {
                    issuancesTimestamps[investor][currentIndex] = issuancesTimestamps[investor][currentIssuancesCount - 1];
                    issuancesValues[investor][currentIndex] = issuancesValues[investor][currentIssuancesCount - 1];
                }

                delete issuancesTimestamps[investor][currentIssuancesCount - 1];
                delete issuancesValues[investor][currentIssuancesCount - 1];

                currentIssuancesCount--;
            } else {
                currentIndex++;
            }
        }

        issuancesCounters[investor] = currentIssuancesCount;
```

Also there don't appear to be any unit tests around this area; I commented out the `while` loop and re-ran the test suite and no tests failed! So ideally before changing anything write some unit tests first to ensure the optimized version doesn't break anything.

**Securitize:** Fixed in commit [10ac116](https://github.com/securitize-io/dstoken/commit/10ac116901001ce804c39aecdadad16b4fc3251c) where we also added additional unit tests around the contents of the `while` loop.

**Cyfrin:** Verified.
