---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-wannabetv2-v2-0-2-10
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-wannabetv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-wannabetv2-v2-0
title: Unresolved developer comments
vuln_class: []
---

# Unresolved developer comments

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-wannabetv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-wannabetv2-v2.0.md)_

---

**Description:** There are leftover developer comments that should be removed or resolved:

`Bet::initialize#L62`:
```solidity
// Maybe can skip this and send it striaght to Aave ?
```

and

`IBbet.Bet#L29`
```solidity
// TODO: I feel like there's a more efficient way to represent the maker:taker ratio
```

The first is misleading (the contract must custody funds itself, not send them directly to Aave as the Aave pool might not be present), and the second is an unresolved `TODO`. Consider removing or clarifying these.

**WannaBet:** Fixed in commit [6bddf7f](https://github.com/gskril/wannabet-v2/commit/6bddf7fc0be929fd10ac731ef87cebba9f7ee686).

**Cyfrin:** Verified.

\clearpage
