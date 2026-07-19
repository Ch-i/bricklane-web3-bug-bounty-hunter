---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-3-28
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: '`Depot` is missing functions present in on-chain deployment'
vuln_class: []
---

# `Depot` is missing functions present in on-chain deployment

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

The `Depot` contract is already [deployed](https://etherscan.io/address/0xDEb0f00071497a5cc9b4A6B96068277e57A82Ae2) and in use; however, this deployed version contains `receive` and `version` functions that are missing from the contract at the current commit hash. It is understood that the contract was updated and these functions were added in a more recent commit.
