---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-3-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-05-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-13-cyfrin-armada-crowdfund-governance-v2-0
title: '`ArmadaTreasuryGov::setOutflowWindow` has no upper bound'
vuln_class: []
---

# `ArmadaTreasuryGov::setOutflowWindow` has no upper bound

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** The lower bound is `>= 1 days` but there is no upper bound. Setting `windowDuration = type(uint256).max` makes the per-window cap effectively a lifetime cap. Tightening is immediate; loosening is delayed by the 24-day activation delay - recovery from a typo therefore requires waiting the full activation delay.

**Impact:** A governance action (accidental or malicious) can self-lockdown the treasury for an effectively indefinite duration.

**Recommended Mitigation:** Add an upper bound:

```solidity
require(windowDuration >= 1 days, "TG: window too short");
require(windowDuration <= 365 days, "TG: window too long");
```

**Armada:** Fixed in commit [4acd7f5](https://github.com/ship-armada/armada-poc/commit/4acd7f50943b023376a2856c61f8e1b6d7e20097).

**Cyfrin:** Verified.
