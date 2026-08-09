---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-3-30
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: Use .call(...) for ETH withdraw rather than .transfer(...)
vuln_class: []
---

# Use .call(...) for ETH withdraw rather than .transfer(...)

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

In commit e15dd1,  method withdrawETH(...) has been added in Contract NarwhalPriceAggregator.sol which uses .transfer() to send all the contacts ETH to the recipient address. 

**Recommendation**: 

It is good practice to avoid using transfer() for sending native coins because this method uses a hardcoded gas amount, which may not be sufficient in the future and can potentially lead to unexpected failures. By using .call.value(...)("") instead, developers have more control over the gas usage and can adapt to changing gas costs, ensuring the robustness of contracts.

**Fix**: Issue fixed in commit a7755
