---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-11-20-cyfrin-mode-earnm-4-3
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-11-20T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-20-cyfrin-mode-earnm.md
tags:
- firm:cyfrin
- report:2023-11-20-cyfrin-mode-earnm
title: State variables should be cached in stack variables rather than re-reading
  them from storage
vuln_class: []
---

# State variables should be cached in stack variables rather than re-reading them from storage

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2023-11-20-cyfrin-mode-earnm.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-20-cyfrin-mode-earnm.md)_

---

**Description:** State variables should be cached in stack variables rather than re-reading them from storage.

* `MysteryBox::fulfillRandomWords()` reads `vrfRequests[_requestId]` 3 times; consider reading it once into memory then reading from memory to avoid multiple storage reads.
* `MysteryBox::fulfillBoxAmount()` could cache `eaRequestToAddress[_requestId]` and also `delete addressToRandomNumber[sender]`
* `MysteryBox::_assignTierAndMint()` should have `uint256 newBoxId = ++boxIdCounter;` then use `newBoxId` in the rest of the function.

**Impact:** Gas optimization

**Recommended Mitigation:** State variables should be cached in stack variables rather than re-reading them from storage.

**Mode:**
Fixed in commit [85b2012](https://github.com/Earnft/smart-contracts/commit/85b20121604b5d162bb14c2c96731b8345ca1cb3), [c4c50ed](https://github.com/Earnft/smart-contracts/commit/c4c50edcd2a3f9fc2da4e1934bcfa1d3cbd85809), [d5b14d8](https://github.com/Earnft/smart-contracts/commit/d5b14d80dae0cc78ab63537d405c8c49a6238a57), [5df2b82](https://github.com/Earnft/smart-contracts/commit/5df2b824dba5b25a0d8db28fa10de4a4bc52ec3b).

**Cyfrin:** Verified.
