---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-11-01-yhairvesting-1-4
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-11-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-11-01-yHairVesting.md
tags:
- firm:pashov-audit-group
- report:2023-11-01-yhairvesting
title: '[L-05] Using the `transfer` function of `address payable` is discouraged'
vuln_class: []
---

# [L-05] Using the `transfer` function of `address payable` is discouraged

_Section severity (from Solodit section header): Low_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-11-01-yHairVesting.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-11-01-yHairVesting.md)_

---

The `release`, `releaseAvailableTokensForHolder` and `purchaseVSchedule` methods in `TokenVestingV2` use the `transfer` method of `address payable` to transfer native asset funds to an address. If the `paymentReceiver` address is a smart contract that has a `receive` or `fallback` function that takes up more than the 2300 gas (which is the limit of `transfer`), then the methods will revert every time until the `paymentReceiver` is changed. Examples are some smart contract wallets or multi-sig wallets, so usage of `transfer` is discouraged. To fix this, use a `call` with value instead of `transfer`. There is also no reentrancy risk as the three methods all use the `nonReentrant` modifier.
