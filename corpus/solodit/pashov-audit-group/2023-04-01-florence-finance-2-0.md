---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-04-01-florence-finance-2-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-04-01T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-04-01-Florence%20Finance.md
tags:
- firm:pashov-audit-group
- report:2023-04-01-florence-finance
title: '[M-01] The Chainlink price feed''s input is not properly validated'
vuln_class: []
---

# [M-01] The Chainlink price feed's input is not properly validated

_Section severity (from Solodit section header): Medium_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-04-01-Florence Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-04-01-Florence%20Finance.md)_

---

**Impact:**
High, as it can result in the application working with an incorrect asset price

**Likelihood:**
Low, as Chainlink oracles are mostly reliable, but there has been occurrences of this issue before

**Description**

The code in `LoanVault::getFundingTokenExchangeRate` uses a Chainlink price oracle in the following way:

```solidity
(, int256 exchangeRate, , , ) = fundingTokenChainLinkFeeds[fundingToken].latestRoundData();

if (exchangeRate == 0) {
    revert Errors.ZeroExchangeRate();
}
```

This has some validation but it does not check if the answer (or price) received was actually a stale one. Reasons for a price feed to stop updating are listed [here](https://ethereum.stackexchange.com/questions/133242/how-future-resilient-is-a-chainlink-price-feed/133843#133843). Using a stale price in the application can result in wrong calculations in the vault shares math which can lead to an exploit from a bad actor.

**Recommendations**

Change the code in the following way:

```diff
- (, int256 exchangeRate, , , ) = fundingTokenChainLinkFeeds[fundingToken].latestRoundData();
+ (, int256 exchangeRate, , uint256 updatedAt , ) = fundingTokenChainLinkFeeds[fundingToken].latestRoundData();

- if (exchangeRate == 0) {
+ if (exchangeRate <= 0) {
    revert Errors.ZeroExchangeRate();
}

+ if (updatedAt < block.timestamp - 60 * 60 /* 1 hour */) {
+   pause();
+}
```

This way you will also check for negative price (as it is of type `int256`) and also for stale price. To implement the pausing mechanism I proposed some other changes will be needed as well, another option is to just revert there.
