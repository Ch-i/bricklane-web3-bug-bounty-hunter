---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-03-27-global-interlink-2-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-03-27T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-03-27-Global%20Interlink.md
tags:
- firm:zokyo
- report:2023-03-27-global-interlink
title: The name of the function can cause a misunderstanding
vuln_class: []
---

# The name of the function can cause a misunderstanding

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-03-27-Global Interlink.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-03-27-Global%20Interlink.md)_

---

**Severity**: Low

**Status**: Resolved

**Description**

In contract utility.move, the function name "get_current_timestamp" could be misunderstood as a Unix timestamp, leading to potential confusion for developers who may rely on this function. It would be better to use a more specific name to avoid any confusion. By modifying the function name to "get_time_from_genesis", it will be clearer to developers that the function is not returning a Unix timestamp, but rather the time since the genesis block. This change will help to reduce confusion and potential errors in code that relies on this function.

**Recommendation**: 

Modify the function name to "get_time_from_genesis" to more accurately reflect the function's purpose of calculating the time since the genesis block. This name will be more specific and easier for developers to understand, avoiding any potential confusion.
