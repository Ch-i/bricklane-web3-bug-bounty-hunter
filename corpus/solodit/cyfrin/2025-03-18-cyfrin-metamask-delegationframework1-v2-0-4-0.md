---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-18-cyfrin-metamask-delegationframework1-v2-0-4-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-03-18T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-18-cyfrin-Metamask-DelegationFramework1-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-18-cyfrin-metamask-delegationframework1-v2-0
title: '`WebAuthn::contains()` optimization'
vuln_class: []
---

# `WebAuthn::contains()` optimization

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-18-cyfrin-Metamask-DelegationFramework1-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-18-cyfrin-Metamask-DelegationFramework1-v2.0.md)_

---

**Description:** In the `WebAuthn::contains()` function, the current implementation checks for out-of-bounds conditions inside the loop on each iteration. This is inefficient as the same check is performed repeatedly.

```solidity
//WebAuthn.sol
function contains(string memory substr, string memory str, uint256 location) internal pure returns (bool) {
    bytes memory substrBytes = bytes(substr);
    bytes memory strBytes = bytes(str);

    uint256 substrLen = substrBytes.length;
    uint256 strLen = strBytes.length;

    for (uint256 i = 0; i < substrLen; i++) {
        if (location + i >= strLen) {
            return false;
        }
        ...
    }

    return true;
}
```

**Recommended Mitigation:** Consider performinga single bounds check before entering the loop. This checks if the substring would fit within the main string at the specified location.

**Metamask:** Acknowledged. Taken from SmoothCyptoLib - will keep this for consistency.

**Cyfrin:** Acknowledged.

\clearpage
