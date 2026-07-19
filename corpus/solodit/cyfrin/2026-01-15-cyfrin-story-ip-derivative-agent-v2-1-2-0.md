---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-15-cyfrin-story-ip-derivative-agent-v2-1-2-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-01-15T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-15-cyfrin-story-ip-derivative-agent-v2.1.md
tags:
- firm:cyfrin
- report:2026-01-15-cyfrin-story-ip-derivative-agent-v2-1
title: '`IPDerivativeAgent::constructor` `owner` check redundant'
vuln_class: []
---

# `IPDerivativeAgent::constructor` `owner` check redundant

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-15-cyfrin-story-ip-derivative-agent-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-15-cyfrin-story-ip-derivative-agent-v2.1.md)_

---

**Description:** The `IPDerivativeAgent::constructor` checks `owner == address(0)` after calling `Ownable(owner)` in the initializer list. Since OpenZeppelin’s `Ownable` constructor already reverts on a zero owner, this custom check is redundant and will never be reached. Consider removing it.

**Story:** Fixed in [PR#5](https://github.com/piplabs/story-ecosystem/pull/5)

**Cyfrin:** Verified.

\clearpage
