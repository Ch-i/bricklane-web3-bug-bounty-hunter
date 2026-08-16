---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-25-cyfrin-button-basis-trade-v2-0-2-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-09-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-25-cyfrin-button-basis-trade-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-25-cyfrin-button-basis-trade-v2-0
title: '`BasisTradeTailor` is ERC-165 non compliant'
vuln_class: []
---

# `BasisTradeTailor` is ERC-165 non compliant

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-25-cyfrin-button-basis-trade-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-25-cyfrin-button-basis-trade-v2.0.md)_

---

**Description:** The `BasisTradeTailor` contract inherits from and implements the `ITailor` interface. According to the ERC-165 standard, the `supportsInterface` function should return `true` when queried with the interface ID of `ITailor` and `IERC1822Proxiable` (coming from `UUPSUpgradeable`).

However, the current implementation of `supportsInterface` only calls `super.supportsInterface(interfaceId)`, which delegates the check to the parent `AccessControlUpgradeable` contract. The parent contract is unaware of the `ITailor` and `IERC1822Proxiable` interfaces and will therefore return `false` for the interface IDs. This means the contract incorrectly reports that it does not support interfaces it actually implements, which can break interactions with other contracts that rely on ERC-165 for interface detection.

**Recommended Mitigation:** The `supportsInterface` function should be updated to explicitly check for the `ITailor` and `IERC1822Proxiable` interface IDs in addition to calling the `super` function. This ensures that the contract correctly advertises its implementation of the given interfaces.

```solidity
// ...existing code...

import {IERC1822Proxiable} from "@openzeppelin/contracts/interfaces/draft-IERC1822.sol";

// ...existing code...

    /**
     * @notice Override supportsInterface to resolve multiple inheritance
     */
    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(AccessControlUpgradeable)
        returns (bool)
    {
        return interfaceId == type(ITailor).interfaceId ||
        return interfaceId == type(IERC1822Proxiable).interfaceId ||
        super.supportsInterface(interfaceId);
    }

// ...existing code...
```

**Button:** Fixed in commit [`32f8ca9`](https://github.com/buttonxyz/button-protocol/commit/32f8ca9c9e08986a554e12d3581178419b3d71f9)

**Cyfrin:** Verified. Recommendation implemented.
