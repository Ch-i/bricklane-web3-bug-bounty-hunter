---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-02-23-cyfrin-swell-barracuda-2-3
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-02-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md
tags:
- firm:cyfrin
- report:2024-02-23-cyfrin-swell-barracuda
title: Refactor identical code in `NodeOperatorRegistry::getNextValidatorDetails`
vuln_class: []
---

# Refactor identical code in `NodeOperatorRegistry::getNextValidatorDetails`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-02-23-cyfrin-swell-barracuda.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md)_

---

**Description:** The bodies of these two `else if` [branches](https://github.com/SwellNetwork/v3-contracts-lst/blob/a95ea7942ba895ae84845ab7fec1163d667bee38/contracts/implementations/NodeOperatorRegistry.sol#L151-L162) are identical:

```solidity
} else if (foundOperatorId == 0) {
  // If no operator has been found yet set the smallest operator active keys to the current operator
  smallestOperatorActiveKeys = operatorActiveKeys;

  foundOperatorId = operatorId;

  // If the current operator has less keys than the smallest operator active keys, then we want to use this operator
} else if (smallestOperatorActiveKeys > operatorActiveKeys) {
  smallestOperatorActiveKeys = operatorActiveKeys;

  foundOperatorId = operatorId;
}
```

Hence the code can be simplified to:
```solidity
// If no operator has been found yet set the smallest operator active keys to the current operator
// If the current operator has less keys than the smallest operator active keys, then we want to use this operator
} else if (foundOperatorId == 0 ||
           smallestOperatorActiveKeys > operatorActiveKeys) {
  smallestOperatorActiveKeys = operatorActiveKeys;
  foundOperatorId = operatorId;
}
```

**Swell:** Fixed in commit [d457d8d](https://github.com/SwellNetwork/v3-contracts-lst/commit/d457d8d109770f86b2b6ab3f785e1678ca341d6f).

**Cyfrin:**
Verified.

\clearpage
