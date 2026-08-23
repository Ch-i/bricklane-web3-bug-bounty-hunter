---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-20-cyfrin-aarc-btcy-v2-0-3-3
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-02-20T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-20-cyfrin-aarc-btcy-v2-0
title: Use named return variables where this can optimize away local variables
vuln_class: []
---

# Use named return variables where this can optimize away local variables

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-20-cyfrin-aarc-btcy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md)_

---

**Description:** Use named return variables where this can optimize away local variables:
* `BTCY::withdraw`
* `Pricer::getPriceIds`

**Aarc:** Fixed in commit [7a26d87](https://github.com/aarc-xyz/btcy-contracts-main/commit/7a26d87b170197f20383f3098f3a16e34ec1ee1f).

**Cyfrin:** Verified.
