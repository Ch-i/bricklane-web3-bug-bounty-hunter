---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-01-cyfrin-metamask-totalbalanceenforcer-v2-0-2-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-09-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-01-cyfrin-metamask-TotalBalanceEnforcer-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-01-cyfrin-metamask-totalbalanceenforcer-v2-0
title: Incorrect contract natspec for ERC1155TotalBalanceChangeEnforcer
vuln_class: []
---

# Incorrect contract natspec for ERC1155TotalBalanceChangeEnforcer

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-01-cyfrin-metamask-TotalBalanceEnforcer-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-01-cyfrin-metamask-TotalBalanceEnforcer-v2.0.md)_

---

**Description:** The contract natspec for `ERC1155TotalBalanceChangeEnforcer` has several instances of incorrect descriptions about how the balance state is stored in the enforcer.

- "Tracks initial balance and accumulates expected increases and decreases per recipient/token pair within a redemption" => which is incorrect as the accumulated expected amounts are stored per recipient-token-tokenID combination.
- "State is shared between enforcers watching the same recipient/token pair" => Again state is shared only for the same recipient-token-tokenID combination.


**Impact:** These comments incorrectly describe the intended design of the `ERC1155TotalBalanceChangeEnforcer`. Including the tokenID here for deriving the storage keys is very important.

**Recommended Mitigation:** Consider modifying the natspec to correctly state that balance storage for ERC1155 enforcer is shared as per the `recipient-token-tokenID` combination.


**Metamask:** Fixed.

**Cyfrin:** Verified.

\clearpage
