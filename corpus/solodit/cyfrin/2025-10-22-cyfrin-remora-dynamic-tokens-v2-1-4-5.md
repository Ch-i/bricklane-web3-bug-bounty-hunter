---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-22-cyfrin-remora-dynamic-tokens-v2-1-4-5
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-10-22T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-22-cyfrin-remora-dynamic-tokens-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-22-cyfrin-remora-dynamic-tokens-v2-1
title: Consider using struct instead of an array for the domestic and foreign child
  tokens
vuln_class: []
---

# Consider using struct instead of an array for the domestic and foreign child tokens

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-22-cyfrin-remora-dynamic-tokens-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-22-cyfrin-remora-dynamic-tokens-v2.1.md)_

---

**Description:** The `CentralToken` code could probably be simplified by using the following data structure for child tokens.


```solidity
    struct Children {
        address domestic;
        address foreign;
    }

    Children private children;
```

This should lead to greater code clarity. Currently one has to remember that 0 = domestic and 1 = foreign.

This helper function could then be used wherever you currently iterate over the children to retain convenience.

```solidity
    function _forEachChild(function(address) internal fn) internal {
        address a = children.domestic; if (a != address(0)) fn(a);
        a = children.foreign;  if (a != address(0)) fn(a);
    }
```


**Remora:** Fixed at commit [f753fac](https://github.com/remora-projects/remora-dynamic-tokens/commit/f753faca15ce9bfdcda3ed690c65aba410a22f37).

**Cyfrin:** Verified.

\clearpage
