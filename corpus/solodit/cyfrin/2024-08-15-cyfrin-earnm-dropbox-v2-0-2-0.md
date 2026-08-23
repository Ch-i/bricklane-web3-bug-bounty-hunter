---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-15-cyfrin-earnm-dropbox-v2-0-2-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-08-15T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-15-cyfrin-earnm-dropbox-v2-0
title: Protocol can collect less or more fees than expected due to constant `claimFee`
  per transaction regardless of how many boxes are claimed
vuln_class: []
---

# Protocol can collect less or more fees than expected due to constant `claimFee` per transaction regardless of how many boxes are claimed

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-15-cyfrin-earnm-dropbox-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md)_

---

**Description:** `DropBox::claimDropBoxes` allows users to pass an array of `boxIds` to claim per transaction while charging a constant `claimFee` per transaction:
```solidity
// Require that the user sends a fee of "claimFee" amount
if (msg.value != claimFee) revert InvalidClaimFee();
```

This means that (not including gas fees):
* claiming 1 box costs the same as claiming 100 boxes, if done in the 1 transaction
* claiming 100 boxes 1-by-1 costs 100x more than claiming 100 boxes in 1 transaction

**Impact:** The protocol will collect:
* less fees if users claim batches of boxes
* more fees if users claim boxes one-by-one

**Recommended Mitigation:** Charge `claimFee` per transaction taking into account the number of boxes being claimed, eg:
```solidity
// Require that the user sends a fee of "claimFee" amount per box
if (msg.value != claimFee * _boxIds.length) revert InvalidClaimFee();
```

**Mode:**
Acknowledged; this was required by the product specification.
