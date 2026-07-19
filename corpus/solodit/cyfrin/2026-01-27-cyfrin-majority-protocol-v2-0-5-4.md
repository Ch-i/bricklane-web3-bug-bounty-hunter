---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-27-cyfrin-majority-protocol-v2-0-5-4
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-01-27T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-27-cyfrin-majority-protocol-v2-0
title: Perform input-related checks prior to reading storage
vuln_class: []
---

# Perform input-related checks prior to reading storage

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-27-cyfrin-majority-protocol-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md)_

---

**Description:** Since reading from storage is expensive, it is more efficient to "fail fast" by performing input-related checks prior to reading storage:

* `SessionManager.sol`:
```solidity
// in `createGame`, perform this check before all the others
require(_promptStrategies.length == _promptHashes.length, ArrayLengthMismatch());
```

**Majority Games:**
Fixed in commit [02b8fd8](https://github.com/Engage-Protocol/engage-protocol/commit/02b8fd81a5098d581332aecc00d28437e2dc631b).

**Cyfrin:** Verified.
