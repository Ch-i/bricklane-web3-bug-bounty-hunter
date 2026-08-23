---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-04-01-florence-finance-2-5
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-04-01T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-04-01-Florence%20Finance.md
tags:
- firm:pashov-audit-group
- report:2023-04-01-florence-finance
title: '[M-06] Multiple centralization attack vectors are present in the protocol'
vuln_class: []
---

# [M-06] Multiple centralization attack vectors are present in the protocol

_Section severity (from Solodit section header): Medium_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-04-01-Florence Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-04-01-Florence%20Finance.md)_

---

**Impact:**
High, as it can result in a rug from the protocol owner

**Likelihood:**
Low, as it requires a compromised or a malicious owner

**Description**

The protocol owner has privileges to control the funds in the protocol or the flow of them.

The `mint` function in `FlorinToken` is callable by the contract owner, which is `FlorinTreasury`, but `FloriNTreasury` has the `transferFlorinTokenOwnership` method. This makes it possible that the `FlorinTreasury` deployer to mint as many `FlorinToken` tokens to himself as he wants, on demand.

The `withdraw` method in `FlorinStaking` works so that the owner can move all of the staked `florinToken` tokens to any wallet, including his.

The `setMDCperFLRperSecond` method in `FlorinStaking` works so that the owner can stop the rewards at any time or unintentionally distribute them in an instant.

The method `setFundingTokenChainLinkFeed` allows the owner to set any address as the new Chainlink feed, so he can use an address that he controls and returns different prices based on rules he decided.

**Recommendations**

Consider removing some owner privileges or put them behind a Timelock contract or governance.
