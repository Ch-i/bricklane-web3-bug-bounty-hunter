---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-15-penguin-karts-0-3
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2022-03-15T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-15-Penguin%20Karts.md
tags:
- firm:zokyo
- report:2022-03-15-penguin-karts
title: Risk of overflow.
vuln_class: []
---

# Risk of overflow.

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2022-03-15-Penguin Karts.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-15-Penguin%20Karts.md)_

---

**Description**

accTokenPerShare calculation utilizes 1e12*1e18*1e32 that is equal to 1e62. Max size of
unsigned integer (256) is 2**256-1 that is ~1e77. With high pool rate and low
rateDenominator such amount can cause an overflow.

**Recommendation**:

Handle or prevent an overflow exception.
