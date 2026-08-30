---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-1-7
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: Issue in generic withdrawal of Tokens
vuln_class: []
---

# Issue in generic withdrawal of Tokens

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Medium

**Status**: Resolved

**Description**

Vester.sol/VesterNLP.sol - In withdrawToken, it withdraws any token including esToken. This can mess up the Vester balances as it is shown that amount of esToken transferred corresponds to a related amount of Vester minted back.

**Recommendation** 

exclude esToken from transfer.

**Fix**:  Require statement added that asserts token being transferred is not indeed the esToken.
