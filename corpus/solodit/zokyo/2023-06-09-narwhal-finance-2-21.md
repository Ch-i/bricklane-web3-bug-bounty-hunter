---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-2-21
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: BaseToken contract can withdrawToken() function allows role gov to be able
  to withdraw tokens.
vuln_class: []
---

# BaseToken contract can withdrawToken() function allows role gov to be able to withdraw tokens.

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**  : Low

**Status**: Resolved

**Recommendations**:

The gov address should be a multisig wallet to avoid malicious gov from withdrawing tokens.

**Fixed**: Issue fixed in commit  3998b5
