---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-4-9
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: More efficient way of checking for empty string in `CommonUtils::isEmptyString`
vuln_class: []
---

# More efficient way of checking for empty string in `CommonUtils::isEmptyString`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** More efficient way of checking for empty string in `CommonUtils::isEmptyString`:
```solidity
function isEmptyString(string memory _str) internal pure returns (bool) {
    return bytes(_str).length == 0;
}
```

**Securitize:** Fixed in commit [22b117a](https://github.com/securitize-io/dstoken/commit/22b117a3514c04b766aa7be6c855683865549e82).

**Cyfrin:** Verified.
