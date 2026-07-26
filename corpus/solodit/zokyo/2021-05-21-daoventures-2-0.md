---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-05-21-daoventures-2-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2021-05-21T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-05-21-DAOventures.md
tags:
- firm:zokyo
- report:2021-05-21-daoventures
title: SPDX license identifier not provided in DVGToken.sol
vuln_class: []
---

# SPDX license identifier not provided in DVGToken.sol

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2021-05-21-DAOventures.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-05-21-DAOventures.md)_

---

**Description**

Trust in smart contracts can be better established if their source code is available. Since
making source code available always touches on legal problems with regards to copyright, the
Solidity compiler encourages the use of machine-readable SPDX license identifiers.

**Recommendation**:

Before publishing, consider adding a comment containing "SPDX-License-Identifier:
<SPDX-License>" to each source file. Use "SPDX-License-Identifier: UNLICENSED" for
non-open-source code. Please see https://spdx.org for more information.
