---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-08-06-mint-gold-dust-2-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2021-08-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-08-06-Mint%20Gold%20Dust.md
tags:
- firm:zokyo
- report:2021-08-06-mint-gold-dust
title: “Magic" numbers
vuln_class: []
---

# “Magic" numbers

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2021-08-06-Mint Gold Dust.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-08-06-Mint%20Gold%20Dust.md)_

---

**Description**

contracts/MGD.sol#213, updateMetadata()
contracts/MGD.sol#360, royaltiInfo()
Variables should be set as constants with proper naming and documentation. That will
increase the code readability and give a chance to verify the functionality in case these
numbers should be adjusted.

**Recommendation**:

Move variables to constants.
