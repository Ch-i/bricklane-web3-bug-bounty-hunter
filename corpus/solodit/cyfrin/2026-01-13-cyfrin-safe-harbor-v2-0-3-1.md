---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-13-cyfrin-safe-harbor-v2-0-3-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-01-13T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-13-cyfrin-safe-harbor-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-13-cyfrin-safe-harbor-v2-0
title: Cache storage to prevent identical storage reads
vuln_class: []
---

# Cache storage to prevent identical storage reads

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-13-cyfrin-safe-harbor-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-13-cyfrin-safe-harbor-v2.0.md)_

---

**Description:** Cache storage to prevent identical storage reads:

* `Agreement.sol`
```solidity
// cache `accts.length` in `getDetails`
320:            _details.chains[i].accounts = new Account[](accts.length);
321:            for (uint256 j = 0; j < accts.length; ++j) {

// cache `chainAccounts.length` in `_findAccountIndex`
398:        for (uint256 i = 0; i < chainAccounts.length; i++) {
```

**SafeHarbor:**
Fixed in commit [eb51eb0](https://github.com/PatrickAlphaC/safe-harbor/commit/eb51eb04669c5c48ca6fa692b2215593f7eae11b).

**Cyfrin:** Verified.
