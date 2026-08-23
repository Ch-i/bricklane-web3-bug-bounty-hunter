---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-2-17
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: Not maximum amount of issuances enforce
vuln_class: []
---

# Not maximum amount of issuances enforce

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** The `createIssuanceInformation` function in `ComplianceServiceRegulated.sol` allows unlimited issuance records to be created per investor without any maximum limit. Unlike the lock system which has a `MAX_LOCKS_PER_INVESTOR = 30` constant to prevent run out of gas, the issuance system has no such protection. Each time tokens are issued to an investor, a new issuance record is created and stored in unbounded mappings (`issuancesValues`, `issuancesTimestamps`, `issuancesCounters`). These records are processed in loops during compliance checks (`getComplianceTransferableTokens` and `cleanupExpiredIssuances`), which could potentially cause gas limit issues if an investor accumulates too many issuance records.

```solidity
function createIssuanceInformation(
        string memory _investor,
        uint256 _shares,
        uint256 _issuanceTime
    ) internal returns (bool) {
        uint256 issuancesCount = issuancesCounters[_investor];//@audit-ok (low) there is not max limit for the issuancesCounters?

        issuancesValues[_investor][issuancesCount] = _shares;
        issuancesTimestamps[_investor][issuancesCount] = _issuanceTime;
        issuancesCounters[_investor] = issuancesCount + 1;

        return true;
    }

```

**Impact:** If an investor accumulates many issuance records, compliance checks could hit gas limits; While the attack vector is limited due to the issuance is an access control operation the lock manager is also an access control operation and have a maximum lock

**Recommended Mitigation:** Implement a maximum limit for issuance records per investor, similar to the existing lock system.

**Securitize:** Acknowledged; the cleanup method was created for this very reason, and we assume that we will clean enough records to avoid hitting those scenarios because lockup periods are not that long that we need to keep very old issuance records.
