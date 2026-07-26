---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-15-cyfrin-veefriends-v2-0-1-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-10-15T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-15-cyfrin-veefriends-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-15-cyfrin-veefriends-v2-0
title: Superfluous unchecked block can be removed
vuln_class: []
---

# Superfluous unchecked block can be removed

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-15-cyfrin-veefriends-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-15-cyfrin-veefriends-v2.0.md)_

---

**Description:** Unchecked blocks in which no arithmetic operation are performed are superfluous and can be removed:

```solidity
function totalMinted() public view returns (uint256) {
    unchecked {
        return _mintCounter;
    }
}

function totalBurned() public view returns (uint256) {
    unchecked {
        return _burnCounter;
    }
}
```

**Recommended Mitigation:**
```diff
function totalMinted() public view returns (uint256) {
-   unchecked {
        return _mintCounter;
-   }
}

function totalBurned() public view returns (uint256) {
-   unchecked {
        return _burnCounter;
-   }
}
```

**VeeFriends:** Fixed in commit [ed976c6](https://github.com/veefriends/smart-contracts-v2/commit/ed976c671033b145b9055337218196dfb2e642ae).

**Cyfrin:** Verified.

\clearpage
