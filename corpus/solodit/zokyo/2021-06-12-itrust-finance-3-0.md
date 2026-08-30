---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-06-12-itrust-finance-3-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2021-06-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-12-iTrust%20Finance.md
tags:
- firm:zokyo
- report:2021-06-12-itrust-finance
title: Consider usage of exponential notation
vuln_class: []
---

# Consider usage of exponential notation

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2021-06-12-iTrust Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-12-iTrust%20Finance.md)_

---

**Description**

There are several places with literals with too many digits. Consider usage of constants for
them with exponential notation. It will increase the readability of the code and decrease the
chance of the typo error in the number of digits.
div(1000000000000000000) (vaults\Burn.sol#115)
div(1000000000000000000) (vaults\StakingData.sol#367)

**Recommendation**:

Use “snake” literals form or use exponential notation.
