---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-10-16-isle-finance-1-5
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-10-16T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-16-Isle%20Finance.md
tags:
- firm:zokyo
- report:2024-10-16-isle-finance
title: Use of Floating Solidity Version (pragma solidity ^0.8.19)
vuln_class: []
---

# Use of Floating Solidity Version (pragma solidity ^0.8.19)

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-10-16-Isle Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-16-Isle%20Finance.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**: 

The current smart contracts use a floating pragma for the Solidity version (pragma solidity ^0.8.19). While this approach allows for compatibility with future minor releases, it introduces potential risks. Future updates might include changes and newly discovered bugs or vulnerabilities that could affect the contract's functionality and security. Locking the Solidity version would ensure the contract behaves consistently as tested and accounts for all known issues at that version.

**Recommendation**: 

It is recommended to specify a fixed Solidity version for your contracts, such as pragma solidity 0.8.19;, instead of using pragma solidity ^0.8.19;. This will ensure that the contract operates as expected without unintended changes due to future compiler updates.

**Comment**: 

Client confirms to follow the recommendation to fix it in order to prevent any existing compiler-related issues.
