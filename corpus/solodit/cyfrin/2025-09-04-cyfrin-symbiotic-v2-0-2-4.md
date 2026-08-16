---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-04-cyfrin-symbiotic-v2-0-2-4
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-09-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-04-cyfrin-symbiotic-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-04-cyfrin-symbiotic-v2-0
title: Inconsistent error handling for empty data
vuln_class: []
---

# Inconsistent error handling for empty data

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-04-cyfrin-symbiotic-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-04-cyfrin-symbiotic-v2.0.md)_

---

**Description:** In `_getSelector()`, when data is empty, it returns `0xEEEEEEEE` which is not a standard practice.

```solidity
function _getSelector(bytes memory data) internal pure returns (bytes4 selector) {
    if (data.length == 0) {
        return 0xEEEEEEEE;
    }
    // ...
}
```

**Impact:** Potentially unexpected return values confusing functions interacting with the `_getSelector` function.

**Recommended Mitigation:** Consider documenting the chosen behaviour so developers and future auditors know whether it is expected behaviour.

**Symbiotic:** Fixed in [8667780](https://github.com/symbioticfi/relay-contracts/pull/36/commits/8667780b0653a83f68a2cdb1c630ad8582eaa787).

**Cyfrin:** Verified.

\clearpage
