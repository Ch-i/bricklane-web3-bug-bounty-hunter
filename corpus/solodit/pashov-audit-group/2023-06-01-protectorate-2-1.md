---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-06-01-protectorate-2-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-06-01T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-06-01-Protectorate.md
tags:
- firm:pashov-audit-group
- report:2023-06-01-protectorate
title: '[M-02] Insufficient input validation can lead to loss of funds'
vuln_class: []
---

# [M-02] Insufficient input validation can lead to loss of funds

_Section severity (from Solodit section header): Medium_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-06-01-Protectorate.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-06-01-Protectorate.md)_

---

**Impact:**
High, as funds might be stuck forever in contracts

**Likelihood:**
Low, as it requires a configuration error from the admin

**Description**

Multiple places in the codebase have insufficient input validation that can lead to stuck funds.

1. The `performanceFee` in `LendingVault` constructor is not validated as it is in the `adjustPerformanceFee` setter
2. The `_duration` parameter in `Vesting::createSchedule` is not validated, it can be too large or too small
3. The `AuctionDetails` set in the constructor of `DutchAuction` has timestamps and prices that can be too large or too small

If either `_duration` in `Vesting` is too big or the difference between `startTime` and `endTime` in `DutchAuction` is too big then funds can be stuck forever in the contracts.

**Recommendations**

Call the `adjustPerformanceFee` method in `LendingVault`'s constructor to use its input validation. When it comes to the `_duration` parameter in `createSchedule`, use a minimum of 7 days and a maximum of for example 2 years.

For the `AuctionDetails` you need to make check multiple things:

1. `startTime` and `endTime` have not passed already
2. `endTime` is after `startTime`
3. `endTime` is not too far away in the future - maybe max of 15 days

Same things for `startPrice` and `minimumPrice`:

1. Check that `minimumPrice` is smaller than `startPrice`
2. Check that their values are not too big
