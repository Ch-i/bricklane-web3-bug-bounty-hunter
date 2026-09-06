---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-12-trzn-finance-2-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-01-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md
tags:
- firm:zokyo
- report:2024-01-12-trzn-finance
title: Missing checks for failures in `getChainlinkPrice` Function in `ERC20PriceOracle_V2`
vuln_class: []
---

# Missing checks for failures in `getChainlinkPrice` Function in `ERC20PriceOracle_V2`

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-01-12-TRZN Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md)_

---

**Severity**: Low

**Status**: Acknowledged

**Description**

The `getChainlinkPrice` function does not include a check for potential failure scenarios when interacting with Chainlink oracles. 

**Recommendations**:

Implement error handling mechanisms to handle potential failures in fetching oracle data.

**Client comment**: If the Chainlink price fetching is down temporarily, it will be reverted and is as intended. However, in the case there is another reason the Chainlink service cannot be used, such as a chance in API service, the service can be continuously operation after updating the Oracle contract. 
In the future, if an error occurs in the implemented method (such as change in price fetching method from Chainlink, or service interruption from Chainlink), it will be updated so that another method can be used.
