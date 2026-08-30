---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-15-cyfrin-earnm-dropbox-v2-0-4-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-08-15T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-15-cyfrin-earnm-dropbox-v2-0
title: Cache storage variables when same values read multiple times
vuln_class: []
---

# Cache storage variables when same values read multiple times

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-15-cyfrin-earnm-dropbox-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md)_

---

**Description:** Cache storage variables when same values read multiple times:

File: `src/DropBox.sol`
```solidity
232:    if (remainingBoxesAmount == 0) revert NoMoreBoxesToMint();
235:    if (remainingBoxesAmount < boxAmount) revert NoMoreBoxesToMint();

329:    if (remainingBoxesAmount == 0) revert NoMoreBoxesToMint();
354:    if (remainingBoxesAmount < oneTimeCodeData.boxAmount) revert NoMoreBoxesToMint();

357:    if (oneTimeCodeRandomWords[otpHash].length == 0) revert InvalidVrfState();
360:    uint256[] memory randomWords = oneTimeCodeRandomWords[otpHash];
```

**Mode:**
Fixed in commit [3cfec7f](https://github.com/Earnft/dropbox-smart-contracts/commit/3cfec7fe5d6c912725e8db5284399b7177df58a3).

**Cyfrin:** Verified.
