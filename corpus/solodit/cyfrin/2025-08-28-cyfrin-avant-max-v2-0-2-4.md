---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-28-cyfrin-avant-max-v2-0-2-4
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-08-28T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-28-cyfrin-avant-max-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-28-cyfrin-avant-max-v2-0
title: Cache identical storage reads
vuln_class: []
---

# Cache identical storage reads

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-28-cyfrin-avant-max-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-28-cyfrin-avant-max-v2.0.md)_

---

**Description:** Reading from storage is expensive; cache identical storage reads:
* `RequestsManager.sol`:
```solidity
// cache `request.amount` in `RequestsManager::completeBurn`
239:    issueToken.burn(_idempotencyKey, address(this), request.amount);
244:    emit BurnRequestCompleted(_id, request.amount, _withdrawalAmount);
```

**Avant:**
Fixed in commit [9bf3b60](https://github.com/Avant-Protocol/Avant-Contracts-Max/commit/9bf3b6041bee7bfeb79f19a90a79e13cf6674afa).

**Cyfrin:** Verified.

\clearpage
