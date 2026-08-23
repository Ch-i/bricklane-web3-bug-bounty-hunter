---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-wannabetv2-v2-0-3-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-wannabetv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-wannabetv2-v2-0
title: Use named return variables where this can eliminate local variables
vuln_class: []
---

# Use named return variables where this can eliminate local variables

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-wannabetv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-wannabetv2-v2.0.md)_

---

**Description:** Use named return variables where this can eliminate local variables:
* `BetFactory::createBet`
* `Bet::_status`

**WannaBet:** Fixed in commit [1c5fb9d](https://github.com/gskril/wannabet-v2/commit/1c5fb9db92808e9165ba0f13fb600ae4bd9f08f3).

**Cyfrin:** Verified.
