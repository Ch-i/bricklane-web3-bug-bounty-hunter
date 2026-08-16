---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-07-01-baton-launchpad-1-2
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-07-01T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-07-01-Baton%20Launchpad.md
tags:
- firm:pashov-audit-group
- report:2023-07-01-baton-launchpad
title: '[M-03] Centralization vulnerabilities are present in the protocol'
vuln_class: []
---

# [M-03] Centralization vulnerabilities are present in the protocol

_Section severity (from Solodit section header): Medium_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-07-01-Baton Launchpad.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-07-01-Baton%20Launchpad.md)_

---

**Severity**

**Impact:**
High, as it can lead to a rug pull

**Likelihood:**
Low, as it requires a compromised or a malicious owner

**Description**

The `owner` of `BatonLaunchpad` has total control of the `nftImplementation` and `feeRate` storage variable values in the contract. This opens up some attack vectors:

1. The `owner` of `BatonLaunchpad` can front-run a `create` call to change the `nftImplementation` contract to one that also has a method with which he can withdraw the mint fees from it, resulting in a "rug pull"
2. The `owner` of `BatonLaunchpad` can change the fee to a much higher value, either forcing the `Nft` minters to pay a huge fee or just to make them not want to mint any tokens.
3. The `owner` of the `Caviar` dependency can call `close` on the `Pair` contract, meaning that the `nftAdd` call in `lockLp` and the `wrap` call in `seedYieldFarm` would revert. This can mean that the locking of LP and the seeding of the yield farm can never complete, meaning the `owner` of the `Nft` contract can never call `withdraw`, leading to stuck ETH in the contract.

**Recommendations**

Make the `nftImplementation` method callable only once, so the value can't be updated after initially set. For the `feeRate` add a `MAX_FEE_RATE` constant value and check that the new value is less than or equal to it. For the `Caviar` dependency issue you can call it with `try-catch` and just complete the locking of LP or seeding of the yield farm if the call throws an error.
