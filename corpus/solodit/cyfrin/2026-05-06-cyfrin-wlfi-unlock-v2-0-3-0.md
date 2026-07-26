---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-06-cyfrin-wlfi-unlock-v2-0-3-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-05-06T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-06-cyfrin-wlfi-unlock-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-06-cyfrin-wlfi-unlock-v2-0
title: Public view functions that are never called internally can be marked `external`
vuln_class: []
---

# Public view functions that are never called internally can be marked `external`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-06-cyfrin-wlfi-unlock-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-06-cyfrin-wlfi-unlock-v2.0.md)_

---

**Description:** `WorldLibertyFinancialRegistry` declares three view functions as `public` even though none of them are invoked from within the contract. Marking them `external` is cheaper because `external` reads calldata directly, whereas `public` must copy arguments to memory to satisfy the internal-call ABI.


```solidity
// WorldLibertyFinancialRegistry.sol#L164-L182
function isLegacyUserAndIsActivated(address _user) public view returns (bool) {
    ...
}

function isLegacyUserAndIsNotActivated(address _user) public view returns (bool) {
    ...
}

function getLegacyUserInfo(address _user) public view returns (LegacyUser memory) {
    return _validateUserAndReturn(_user);
}
```

None of these three functions are called anywhere else in the contract. `isLegacyUser` (L157) is the only sibling view that must remain `public`, because it is invoked internally from `wlfiReallocateFrom` (L64, L67) and `agentBulkRemoveLegacyUsers` (L140).

**Impact:** Minor gas overhead on every external call to these getters, and a small consistency issue — the other getters in the same section (`nonce`, `getLegacyUserCategory`, `getLegacyUserAllocation`) are already declared `external`.

**Recommended Mitigation:** Change the visibility of the three functions listed above from `public` to `external`.

```solidity
function isLegacyUserAndIsActivated(address _user) external view returns (bool) { ... }
function isLegacyUserAndIsNotActivated(address _user) external view returns (bool) { ... }
function getLegacyUserInfo(address _user) external view returns (LegacyUser memory) { ... }
```

Leave `isLegacyUser` as `public` since it is consumed internally.

**WLFI:** Fixed in commit [1430e24](https://github.com/worldliberty/usd1-protocol/commit/1430e245349795921bebe275f6bd1d835d9f8fa3).

**Cyfrin:** Verified.

\clearpage
