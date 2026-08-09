---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-12-cyfrin-paladin-valkyrie-v2-0-3-6
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-03-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-12-cyfrin-paladin-valkyrie-v2-0
title: Inability to remove hooks and Incentive Systems from the Incentive Manager
vuln_class: []
---

# Inability to remove hooks and Incentive Systems from the Incentive Manager

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-12-cyfrin-paladin-valkyrie-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md)_

---

**Description:** It is understood that there is currently no mechanism for removing hooks and Incentive Systems from the Incentive Manager to avoid potential sync and notification issues. However, if a bug or some other attack is discovered on one of these contracts that causes them to misbehave, it may be pertinent to consider implementing pausing functionality or some other type of freezing mechanism that prevents specific actions (e.g. deposits in the Hooks, depositing rewards, etc).

**Paladin:** Fixed by commit [`9d6cbff`](https://github.com/PaladinFinance/Valkyrie/pull/5/commits/9d6cbffca07145358c5ceef54d772267fadf5604).

**Cyfrin:** Verified. The logic contract are now pauseable and individual listed hooks can be frozen.

\clearpage
