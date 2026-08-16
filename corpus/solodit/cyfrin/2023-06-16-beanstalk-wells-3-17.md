---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-06-16-beanstalk-wells-3-17
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-06-16T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-16-Beanstalk%20wells.md
tags:
- firm:cyfrin
- report:2023-06-16-beanstalk-wells
title: Time Weighted Average Price oracles are susceptible to manipulation
vuln_class: []
---

# Time Weighted Average Price oracles are susceptible to manipulation

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-06-16-Beanstalk wells.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-16-Beanstalk%20wells.md)_

---

It should be noted that on-chain TWAP oracles are [susceptible to manipulation](https://eprint.iacr.org/2022/445.pdf). Using them to power critical parts of any on-chain protocol is [potentially dangerous](https://blog.openzeppelin.com/secure-smart-contract-guidelines-the-dangers-of-price-oracles/).

**Beanstalk:** This is our best attempt at a manipulation-resistant oracle. Manipulation will always be possible, but we believe that there is significant protection against Oracle manipulation in our implementation.

**Cyfrin:** Acknowledged.

\clearpage
