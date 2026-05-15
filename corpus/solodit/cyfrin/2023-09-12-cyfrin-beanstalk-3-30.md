---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-3-30
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: '`Root.sol` should be updated to be compatible with recent changes to Beanstalk'
vuln_class: []
---

# `Root.sol` should be updated to be compatible with recent changes to Beanstalk

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

It is understood that `Root.sol` is wholly commented out due to incompatibility with more recent changes to the core Beanstalk system. This should be resolved such that the upgradeable Root contract is once again compatible with the current iteration of Beanstalk and users can interact with wrapped Silo deposits as intended.
