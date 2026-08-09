---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2022-12-23-rysk-uniswapv3rangeorderreactor-3-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2022-12-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-23-rysk%20UniswapV3RangeOrderReactor.md
tags:
- firm:trust-security
- report:2022-12-23-rysk-uniswapv3rangeorderreactor
title: Safety checks
vuln_class: []
---

# Safety checks

_Section severity (from Solodit section header): Informational_  
_Audit firm: Trust Security_  
_Source report: [2022-12-23-rysk UniswapV3RangeOrderReactor.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-23-rysk%20UniswapV3RangeOrderReactor.md)_

---

The contract is somewhat lacking in safety checks. fulfillActiveRangeOrder does not verify 
the contract is in active position. Addresses should not be zero. The oracle calculated price 
should be close to pool-generated price. Additional checks will increase the robustness of 
the contract when moving forward.
