---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-3-11
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-05-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-13-cyfrin-armada-crowdfund-governance-v2-0
title: '`transferTo, transferETHTo` in `standardSelectors` but wind-down-only'
vuln_class: []
---

# `transferTo, transferETHTo` in `standardSelectors` but wind-down-only

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** Both functions require `msg.sender == windDownContract`. Listing them in `standardSelectors` creates an apparent governance path that always reverts silently.

**Impact:** Proposal authors may encounter confusing revert behaviour when trying to classify these as standard actions.

**Recommended Mitigation:** Remove them from `standardSelectors`.

**Armada:** Fixed in commit [55cca00](https://github.com/ship-armada/armada-poc/commit/55cca00d6886ce18a5f035267f69e9e8e277db8d).

**Cyfrin:** Verified.
