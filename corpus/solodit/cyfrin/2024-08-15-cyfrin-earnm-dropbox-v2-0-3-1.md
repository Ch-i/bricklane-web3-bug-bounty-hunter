---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-15-cyfrin-earnm-dropbox-v2-0-3-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-08-15T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-15-cyfrin-earnm-dropbox-v2-0
title: Avoid floating pragma unless creating libraries
vuln_class: []
---

# Avoid floating pragma unless creating libraries

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-15-cyfrin-earnm-dropbox-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md)_

---

**Description:** Per [SWC-103](https://swcregistry.io/docs/SWC-103/) compiler versions in pragmas should be fixed unless creating libraries. Choose a specific compiler version to use for development, testing and deployment, eg:
```diff
- pragma solidity ^0.8.19;
+ pragma solidity 0.8.19;
```

**Mode:**
Fixed in commit [668011e](https://github.com/Earnft/dropbox-smart-contracts/commit/668011ebd393dd1c224b2236e70fc9d0bf043e77).

**Cyfrin:** Verified.
