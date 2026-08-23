---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-11-03-cyfrin-streamr-1-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-11-03T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-03-cyfrin-streamr.md
tags:
- firm:cyfrin
- report:2023-11-03-cyfrin-streamr
title: Operators can bypass a `leavePenalty` using `reduceStakeTo()`
vuln_class: []
---

# Operators can bypass a `leavePenalty` using `reduceStakeTo()`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2023-11-03-cyfrin-streamr.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-03-cyfrin-streamr.md)_

---

**Severity:** Medium

**Description:** Operators should pay a leave penalty when they unstake earlier than expected.
But there are no relevant requirements in `reduceStakeTo()` so they can reduce their staking amount to the minimum value.

- An operator staked 100 and he wants to unstake earlier.
- When he calls `forceUnstake()`, he should pay `100 * 10% = 10` as a penalty.
- But if he reduces the staking amount to the minimum(like 10) using `reduceStakeTo()` first and calls `forceUnstake()`, the penalty will be `10 * 10% = 1.`

**Impact:** Operators will pay a `leavePenalty` for the minimum amount only.

**Recommended Mitigation:** The penalty should be the same, whether an Operator only calls `forceUnstake`, or first calls `reduceStakeTo`.

**Client:** Fixed in commit [72323d0](https://github.com/streamr-dev/network-contracts/commit/72323d0099a85c8c7a5d59335492eebcc9cc66bb).

**Cyfrin:** Verified
