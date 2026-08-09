---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-5-4
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-03-25T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-25-cyfrin-sablier-bob-escrow-v2-0
title: Use named return variables where this can optimize away local variables
vuln_class: []
---

# Use named return variables where this can optimize away local variables

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md)_

---

**Description:** Use named return variables where this can optimize away local variables:
* `SablierBob::_safeTokenSymbol`

**Sablier:** Fixed in commit [0c05295](https://github.com/sablier-labs/lockup/commit/0c05295253e369d1d0549ebd7256b3807313cd3a).

**Cyfrin:** Verified.
