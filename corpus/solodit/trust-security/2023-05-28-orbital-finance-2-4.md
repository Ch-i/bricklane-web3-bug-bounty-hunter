---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-05-28-orbital-finance-2-4
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-05-28T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-28-Orbital%20Finance.md
tags:
- firm:trust-security
- report:2023-05-28-orbital-finance
title: TRST-L-5 When owner is also the operator, they can drain all funds in a vault
vuln_class: []
---

# TRST-L-5 When owner is also the operator, they can drain all funds in a vault

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-05-28-Orbital Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-28-Orbital%20Finance.md)_

---

**Description:** 
The code changes implemented to fix slippage changes introduced a significant centralization 
risk. The owner can change price feeds at any time.
```solidity
         function addPriceFeed(address token, address priceFeed) external  onlyOwner {
         // require(aggregatorAddresses[token] == address(0), "price feed exists");
               aggregatorAddresses[token] = priceFeed;
                  emit PriceFeedAdded(token, priceFeed, true);
         }
         function removePriceFeed(address token) external onlyOwner {
             aggregatorAddresses[token] = address(0);
                emit PriceFeedAdded(token, address(0), false);
         }
```
This can be used to skew the minimum to receive value queried in `trade()`:
```solidity
      //check slippage with chainlink oracle
      uint256 maxSlippage = AI.getPairMaxSlippage(params.spendToken, params.receiveToken);
         require(CLI.getMinReceived(params.spendToken, params.receiveToken, 
            params.spendAmt, maxSlippage) <= params.receiveAmtMin, "rec min too low");
```
Therefore, owner can perform the sandwich attack detailed under "Autotrader can steal 
funds". He would need to double as the operator or the autotrader.
