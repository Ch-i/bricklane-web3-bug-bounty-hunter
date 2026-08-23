---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-06-radiant-capital-0-5
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2022-03-06T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md
tags:
- firm:zokyo
- report:2022-03-06-radiant-capital
title: Price can be manipulated via flashloans.
vuln_class: []
---

# Price can be manipulated via flashloans.

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2022-03-06-Radiant Capital.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md)_

---

**Description**

PriceProvider.sol: update(), getToken Price(), getLpToken Price(). 
Since the contract calculates the price based on a single DEX (Uniswap or Balancer), it can be manipulated via flashloans. There are several parts of the protocol where price manipulation is profitable for an attacker. 
1. Disqualifier.sol: getBaseBounty(). 
When a provided user can be disqualified, the contract calculates a bounty for him based on the price of RDNT. Though the calculated bounty can't exceed 'maxBaseBounty', the attacker can manipulate the price to receive the maximum allowed bounty. 
2. RadiantOFT.sol: _getBridgeFee(). 
The contract utilizes price to calculate the fee for using the bridge. In this case, an attacker can manipulate the price to pay lower fees. 
3. EligibilityDataProvider.sol: _locked UsdValue(). 
Price is used to calculate the locked user's amount. In this case, an attacker may use flashloan to manipulate the value of the user's locked funds and affect the disqualification of user. 
The issue is marked as high due to point 3, where users can be affected and disqualified due to price manipulation. 

**Recommendation**: 

Consider using off-chain oracles for price calculation OR use several sources for retrieving price (such as Uniswap, Balancer, Curve) and calculate a Volume Weighted Average Price OR calculate a historical price price based on a single source of price (TWAP). This can help reduce the chances of flashloan attack on the PriceProvider. 

**Post-audit**: 
TWAP oracles based on Uniswap V2 and Uniswap V3 were implemented.
