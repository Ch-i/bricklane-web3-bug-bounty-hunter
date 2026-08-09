---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2022-12-14-vagabond-token-transmuter-2-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2022-12-14T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-14-Vagabond%20Token%20Transmuter.md
tags:
- firm:trust-security
- report:2022-12-14-vagabond-token-transmuter
title: TRST-L-4 tokenDecimalDivider implementation causes limited functionality
vuln_class: []
---

# TRST-L-4 tokenDecimalDivider implementation causes limited functionality

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2022-12-14-Vagabond Token Transmuter.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-14-Vagabond%20Token%20Transmuter.md)_

---

**Description:**
tokenDecimalDivider stores the decimals difference between input token and output token. 
However, this value assumes input decimals is always larger or equal to output decimals. As 
a result, the contract cannot be used for many input/output token pairs.
 ```solidity
         uint256 allocation = (_inputTokenAmount * linearMultiplier) / 
             tokenDecimalDivider;
```

**Mitgation review:**
Add a boolean state variable which will describe whether to divide or multiply by 
tokenDecimalDivider.

**Team response:**
Acknowledged, but will not be fixed at this time as use case does not require division.
