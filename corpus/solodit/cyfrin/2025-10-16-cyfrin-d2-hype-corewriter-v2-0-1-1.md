---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-16-cyfrin-d2-hype-corewriter-v2-0-1-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-10-16T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-d2-hype-corewriter-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-16-cyfrin-d2-hype-corewriter-v2-0
title: Consider using constants instead of magic numbers for action IDs
vuln_class: []
---

# Consider using constants instead of magic numbers for action IDs

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-16-cyfrin-d2-hype-corewriter-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-d2-hype-corewriter-v2.0.md)_

---

**Description:** The action IDs that are used to interact with HyperCore are currently hardcoded in Hype.sol module's functions.

For example, action ID = 6 represents the `spotSend` action:
```solidity
function hyper_sendSpot(
        uint64 asset,
        uint64 _wei
    ) external onlyRole(EXECUTOR_ROLE) nonReentrant {
        sendAction(6, abi.encode(assetAddress(asset), asset, _wei));
    }
```

**Impact:** While this poses no risk, using constants instead of magic numbers improve code maintainability and readability to explain the magic number's intended purpose.

**Recommended Mitigation:** Consider implementing constants for each action ID hardcoded currently. For example, an action ID of 1 can be named as constant `LIMIT_ORDER_ACTION_ID`

**D2:** Fixed in commit [`41470c6`](https://github.com/d2sd2s/d2-contracts/commit/41470c60bd928fb6e67d0db285ef32f0b6490197)

**Cyfrin:** Verified.
