---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-15-cyfrin-earnm-dropbox-v2-0-3-6
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-08-15T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-15-cyfrin-earnm-dropbox-v2-0
title: Use named `mapping` parameters
vuln_class: []
---

# Use named `mapping` parameters

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-15-cyfrin-earnm-dropbox-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md)_

---

**Description:** Solidity 0.8.18 [introduced](https://soliditylang.org/blog/2023/02/01/solidity-0.8.18-release-announcement/) named `mapping` parameters; use this feature in `DropBox` for clearer mappings like this:
```solidity
  /// @notice Mappings
  mapping(uint256 boxId => Box boxData) internal boxIdToBox;
  mapping(bytes32 code => bool usedInd) internal oneTimeCodeUsed; // ensure uniqueness of one-time codes
  mapping(bytes32 codeAddressHash => OneTimeCode codeData) internal oneTimeCode; // ensure integrity of one-time code data
  mapping(bytes32 codeAddressHash => uint256[] randomWords) internal oneTimeCodeRandomWords;
  mapping(uint256 vrfRequestId => bytes32 codeAddressHash) internal activeVrfRequests;
  mapping(uint256 vrfRequestId => bool fulfilledInd) internal fulfilledVrfRequests;
```

**Mode:**
Fixed in commit [8f6a168](https://github.com/Earnft/dropbox-smart-contracts/commit/8f6a168a9ddf17d0b0611c305fa8a0f3069ea56d).

**Cyfrin:** Verified.

\clearpage
