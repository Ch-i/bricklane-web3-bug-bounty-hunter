---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-18-cyfrin-metamask-delegationframework1-v2-0-2-4
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-03-18T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-18-cyfrin-Metamask-DelegationFramework1-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-18-cyfrin-metamask-delegationframework1-v2-0
title: Inconsistent timestamp range validation in `TimestampEnforcer`
vuln_class: []
---

# Inconsistent timestamp range validation in `TimestampEnforcer`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-18-cyfrin-Metamask-DelegationFramework1-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-18-cyfrin-Metamask-DelegationFramework1-v2.0.md)_

---

**Description:** The `TimestampEnforcer` contract allows the creation of delegations with a time-based validity window. However, it lacks validation to ensure logical consistency of the time range.

Specifically, when both the "after" and "before" thresholds are specified, there is no check to ensure that `timestampBeforeThreshold_` is greater than `timestampAfterThreshold_`.

```solidity
//TimeStampEnforcer.sol

function getTermsInfo(bytes calldata _terms)
    public
    pure
    returns (uint128 timestampAfterThreshold_, uint128 timestampBeforeThreshold_)
{
    require(_terms.length == 32, "TimestampEnforcer:invalid-terms-length");
    timestampBeforeThreshold_ = uint128(bytes16(_terms[16:]));
    timestampAfterThreshold_ = uint128(bytes16(_terms[:16]));
}
```

When both timestamps are non-zero, there is an independent check as follows

```solidity
//TimeStampEnforcer.sol

require(block.timestamp > timestampAfterThreshold_, "TimestampEnforcer:early-delegation");
require(block.timestamp < timestampBeforeThreshold_, "TimestampEnforcer:expired-delegation");
//@audit no check on validity of the range
```
This creates a potential for inconsistent time ranges where the "after" threshold is greater than the "before" threshold, resulting in a permanently unusable delegation.

**Impact:** Delegations can be created that appear valid but can never be exercised because of impossible time constraints.

**Recommended Mitigation:** Consider adding a validation check in the `getTermsInfo` function to ensure that when both timestamp thresholds are non-zero, the "before" threshold is greater than the "after" threshold.

**Metamask:** Acknowledged. It is on the delegator to create the correct terms for the delegation.

**Cyfrin:** Acknowledged.

\clearpage
