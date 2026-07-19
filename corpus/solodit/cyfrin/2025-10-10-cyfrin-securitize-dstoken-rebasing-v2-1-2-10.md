---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-2-10
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: Stale Issuance Records After `Burn` and `Seize` Operations
vuln_class: []
---

# Stale Issuance Records After `Burn` and `Seize` Operations

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** The `recordBurn()` and `recordSeize()` functions in `ComplianceServiceRegulated.sol` do not clean up issuance records when tokens are burned or seized. This causes stale issuance records to persist in the system, which can lead to incorrect lock calculations for newly issued tokens. The `cleanupInvestorIssuances()` function only removes expired issuance records based on lock periods, but does not remove records for tokens that have been completely burned or seized.

```solidity
   function recordBurn(address _who, uint256 _value) internal override returns (bool) {

        if (compareInvestorBalance(_who, _value, _value)) {
            adjustTotalInvestorsCounts(_who, CommonUtils.IncDec.Decrease);
        }
        return true;
    }
```

**Impact:** Issuance records remain in the system for tokens that no longer exist, When an investor receives new tokens after a burn/seize operation, the lock calculation in `getComplianceTransferableTokens()` will include stale issuance records from the previously burned/seized tokens

**Proof of Concept:**
 1. Investor receives 100 tokens at timestamp T1 - Creates issuance record: {value: 100, timestamp: T1}
 2. All 100 tokens are burned via burn() function
       - recordBurn() is called but does NOT clean up issuance records
       - Stale issuance record persists: {value: 100, timestamp: T1}
3. Investor receives 50 new tokens at timestamp T2 (after lock period)
    - Creates new issuance record: {value: 50, timestamp: T2}
 4. When calculating transferable tokens, `getComplianceTransferableTokens()` uses BOTH records:
   - Stale record: 100 tokens from T1 (should not exist)
   - New record: 50 tokens from T2
5. If lock period hasn't expired since T1, ALL 150 tokens are considered locked
6. Result: Investor cannot transfer any of their 50 new tokens due to stale lock calculation


**Recommended Mitigation:** Delete the old issuance when a investor is complete burn or seize.

**Securitize:** Acknowledged; generally it is impossible to determine what issuance record should be deleted when a burn or seize occurs, unless there is only 1 issuance record and the burn or seize is for all its tokens. We also have some compliance rules which effectively prevent the described scenario from happening in the first place.
