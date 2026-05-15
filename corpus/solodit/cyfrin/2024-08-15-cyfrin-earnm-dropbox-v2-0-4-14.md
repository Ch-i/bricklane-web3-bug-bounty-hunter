---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-15-cyfrin-earnm-dropbox-v2-0-4-14
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-08-15T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-15-cyfrin-earnm-dropbox-v2-0
title: Simplify checks to fail faster and remove negation operator on final boolean
  result
vuln_class: []
---

# Simplify checks to fail faster and remove negation operator on final boolean result

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-15-cyfrin-earnm-dropbox-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md)_

---

**Description:** Many checks in the code use a pattern of:
```solidity
if( !(check_1 && check_2 && check_3) ) revert Error();
```

Often these checks can be simplified with improved efficiency by re-writting to:
* use `||`  instead of `&&` which makes the check fail sooner, avoiding evaluation of subsequent components
* removes the need for the final `!` negation operator

File: `src/DropBox.sol`
```diff
// L218
- if (!(boxAmount > 0 && boxAmount <= MAX_BOX_AMOUNT_PER_REVEAL)) revert InvalidBoxAmount();
+ if(boxAmount == 0 || boxAmount > MAX_BOX_AMOUNT_PER_REVEAL) revert InvalidBoxAmount();

// L347
- if (!(oneTimeCodeData.boxAmount > 0 && oneTimeCodeData.boxAmount <= MAX_BOX_AMOUNT_PER_REVEAL)) {
+ if (oneTimeCodeData.boxAmount == 0 || oneTimeCodeData.boxAmount > MAX_BOX_AMOUNT_PER_REVEAL) {

// L417
- if (!(_boxIds.length > 0)) revert Unauthorized();
+ if (boxIds.length == 0) revert Unauthorized();

// L442
- if (!(ownerOf(_boxIds[i]) == msg.sender)) revert Unauthorized();
+ if (ownerOf(_boxIds[i]) != msg.sender) revert Unauthorized();
```

File: `src/DropBoxFractalProtocol.sol`
```diff
// L170
- if (!(boxTierId > 0 && boxTierId <= tierIdsLength)) revert InvalidTierId();
+ if (boxTierId == 0 || boxTierId > tierIdsLength) revert InvalidTierId();

// L173
- if (!(boxMintedTimestamp <= block.timestamp && boxMintedTimestamp > 0)) revert InvalidBlockTimestamp();
+ if (boxMintedTimestamp > block.timestamp || boxMintedTimestamp == 0) revert InvalidBlockTimestamp();
```

**Mode:**
Fixed in commit [96773b9](https://github.com/Earnft/dropbox-smart-contracts/commit/96773b972fafd3086a18ad03e65c7199695b5577).

**Cyfrin:** Verified.
