---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-13-cyfrin-safe-harbor-v2-0-3-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2026-01-13T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-13-cyfrin-safe-harbor-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-13-cyfrin-safe-harbor-v2-0
title: Don't cache `calldata` array length
vuln_class: []
---

# Don't cache `calldata` array length

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-13-cyfrin-safe-harbor-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-13-cyfrin-safe-harbor-v2.0.md)_

---

**Description:** It is [cheaper not to cache `calldata` array length](https://github.com/devdacian/solidity-gas-optimization?tab=readme-ov-file#6-dont-cache-calldata-length-effective-009-cheaper) (which is another reason why it is better to use `calldata` for input read-only arrays than `memory`):
* `ChainValidator::setvalidChains, setInvalidChains`

**SafeHarbor:**
Fixed in commit [af8cbc7](https://github.com/PatrickAlphaC/safe-harbor/commit/af8cbc70851ffcf1fb8d393e8fb91e7ad077ad70).

**Cyfrin:** Verified.

\clearpage
