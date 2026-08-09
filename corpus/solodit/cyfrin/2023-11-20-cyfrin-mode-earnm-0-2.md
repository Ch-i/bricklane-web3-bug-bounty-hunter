---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-11-20-cyfrin-mode-earnm-0-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-11-20T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-20-cyfrin-mode-earnm.md
tags:
- firm:cyfrin
- report:2023-11-20-cyfrin-mode-earnm
title: Broken check in `MysteryBox::fulfillRandomWords()` fails to prevent same request
  being fulfilled multiple times
vuln_class: []
---

# Broken check in `MysteryBox::fulfillRandomWords()` fails to prevent same request being fulfilled multiple times

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2023-11-20-cyfrin-mode-earnm.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-20-cyfrin-mode-earnm.md)_

---

**Description:** Consider the [check](https://github.com/Earnft/smart-contracts/blob/43d3a8305dd6c7325339ed35d188fe82070ee5c9/contracts/MysteryBox.sol#L221-L222) which attempts to prevent the same request from being fulfilled multiple times:
```solidity
if (vrfRequests[_requestId].fulfilled) revert InvalidVrfState();
```

The problem is that `vrfRequests[_requestId].fulfilled` is never set to `true` anywhere and `vrfRequests[_requestId]` is [deleted](https://github.com/Earnft/smart-contracts/blob/43d3a8305dd6c7325339ed35d188fe82070ee5c9/contracts/MysteryBox.sol#L244-L245) at the end of the function.

**Impact:** The same request can be fulfilled multiple times which would override the previous randomly generated seed; a malicious provider who was also a mystery box minter could generate new randomness until they got a rare mystery box.

**Recommended Mitigation:** Set `vrfRequests[_requestId].fulfilled = true`.

Consider an optimized version which involves having 2 mappings `activeVrfRequests` and `fulfilledVrfRequests`:
* revert `if(fulfilledVrfRequests[_requestId])`
* else set `fulfilledVrfRequests[_requestId] = true`
* fetch the matching active request into memory from `activeVrfRequests[_requestId]` and continue processing as normal
* at the end `delete activeVrfRequests[_requestId]`

This only stores forever the `requestId` : `bool` pair in `fulfilledVrfRequests`.

Consider a similar approach in `MysteryBox::fulfillBoxAmount()`.

**Mode:**
Fixed in commit [85b2012](https://github.com/Earnft/smart-contracts/commit/85b20121604b5d162bb14c2c96731b8345ca1cb3), [c4c50ed](https://github.com/Earnft/smart-contracts/commit/c4c50edcd2a3f9fc2da4e1934bcfa1d3cbd85809), [d5b14d8](https://github.com/Earnft/smart-contracts/commit/d5b14d80dae0cc78ab63537d405c8c49a6238a57), [5df2b82](https://github.com/Earnft/smart-contracts/commit/5df2b824dba5b25a0d8db28fa10de4a4bc52ec3b).

**Cyfrin:** Verified.
