---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-07-01-baton-launchpad-0-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-07-01T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-07-01-Baton%20Launchpad.md
tags:
- firm:pashov-audit-group
- report:2023-07-01-baton-launchpad
title: '[C-01] Protocol fees from NFT mints can''t be claimed in `BatonLaunchpad`'
vuln_class: []
---

# [C-01] Protocol fees from NFT mints can't be claimed in `BatonLaunchpad`

_Section severity (from Solodit section header): High_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-07-01-Baton Launchpad.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-07-01-Baton%20Launchpad.md)_

---

**Severity**

**Impact:**
High, as it results in a loss of value for the protocol

**Likelihood:**
High, as it certain to happen

**Description**

In `Nft::mint` the `msg.value` expected is the price of an NFT multiplied by the amount of NFTs to mint plus a protocol fee. This protocol fee is sent to the `BatonLaunchpad` contract in the end of the `mint` method like this:

```solidity
if (protocolFee != 0) {
    address(batonLaunchpad).safeTransferETH(protocolFee);
}
```

`BatonLaunchpad` defines a `receive` method that is marked as `payable`, which is correct. The problem is that in `BatonLaunchpad` there is no way to get the ETH balance out of it - it can't be spent in any way possible, leaving it stuck in the contract forever.

**Recommendations**

In `BatonLaunchpad` add a method by which the `owner` of the contract can withdraw its ETH balance.
