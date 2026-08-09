---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-2-20
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: Missing Validations and events in Critical functionality of PriceAggregator
  Contract
vuln_class: []
---

# Missing Validations and events in Critical functionality of PriceAggregator Contract

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**  : Low

**Status**: Resolved

**Description**:


setUSDTFeed function: The function lacks input validation, which means that any value can be passed to it, potentially causing unexpected behavior or errors in the system. It would be best to validate the input to ensure that it is a valid feed address before setting it.
setOracle function: Similar to setUSDTFeed, this function also lacks input validation, allowing any address to be set as the oracle address, which could result in unexpected behavior or errors. Additionally, the function does not emit an event, making it difficult to track changes made to the oracle address.
setAge function: The function has input validation to prevent the age value from exceeding a certain limit. However, it does not emit an event, making it difficult to track changes made to the age value.
setNarwhalTrading function: The function lacks input validation, allowing any address to be set as the NarwhalTrading address, which could result in unexpected behaviour or errors. Additionally, the function does not emit an event, making it difficult to track changes made to the NarwhalTrading address.

**Recommendations** : 

For the setUSDTFeed function:
Add a check to ensure that the _feed parameter is not equal to zero.
Emit an event after setting the new feed.
For the setOracle function:
Add a check to ensure that the _oracle parameter is not equal to zero.
Emit an event after setting the new oracle.
For the setAge function:
Add a check to ensure that the _age parameter is not greater than 60.
Emit an event after setting the new age.
For the setNarwhalTrading function:
Add a check to ensure that the _NarwhalTrading parameter is not equal to zero.
Emit an event after setting the new NarwhalTrading address.

**Fixed**: Issue fixed in commit a72e06b
