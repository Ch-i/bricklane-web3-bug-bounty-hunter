---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-15-cyfrin-earnm-dropbox-v2-0-3-3
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-08-15T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-15-cyfrin-earnm-dropbox-v2-0
title: Use constant `TIER_IDS_LENGTH` in constructor inputs
vuln_class: []
---

# Use constant `TIER_IDS_LENGTH` in constructor inputs

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-15-cyfrin-earnm-dropbox-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md)_

---

**Description:** Use constant `TIER_IDS_LENGTH` in constructor inputs:
```solidity
// DropBox:
  constructor(
    uint256 _subscriptionId,
    address _vrfCoordinator,
    address _feesReceiverAddress,
    string memory __baseTokenURI,
    string memory __contractURI,
    address _earmmERC20Token,
    bytes32 _keyHash,
    address _apiAddress,
    uint24[TIER_IDS_LENGTH] memory _tierTokens,
    uint16[TIER_IDS_LENGTH] memory _tierMaxBoxes,
    string[TIER_IDS_LENGTH] memory _tierNames
  )

// DropBoxFractalProtocol:
  constructor(uint24[TIER_IDS_LENGTH] memory tierTokens,
              uint16[TIER_IDS_LENGTH] memory tierMaxBoxes,
              string[TIER_IDS_LENGTH] memory tierNames) {
```

**Mode:**
Fixed in commit [d8af391](https://github.com/Earnft/dropbox-smart-contracts/commit/d8af391035ca785e2c280de4577f79de2ffda59d).

**Cyfrin:** Verified.
