---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-wannabetv2-v2-0-2-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-wannabetv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-wannabetv2-v2-0
title: Use named mappings to explicitly indicate the purpose of keys and values
vuln_class: []
---

# Use named mappings to explicitly indicate the purpose of keys and values

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-wannabetv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-wannabetv2-v2.0.md)_

---

**Description:** Use named mappings to explicitly indicate the purpose of keys and values:
```
BetFactory.sol
22:    mapping(address => address) public tokenToPool;
```

**WannaBet:** Fixed in commit [a20d1e7](https://github.com/gskril/wannabet-v2/commit/a20d1e7acfbeee00cc891324b022fcf0afdd721b).

**Cyfrin:** Verified.
