---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-14-cyfrin-goldilocks-v1-1-4-4
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-04-14T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md
tags:
- firm:cyfrin
- report:2024-04-14-cyfrin-goldilocks-v1-1
title: Cache array length outside of loops and consider unchecked loop incrementing.
vuln_class: []
---

# Cache array length outside of loops and consider unchecked loop incrementing.

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-14-cyfrin-goldilocks-v1.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md)_

---

```solidity
File: Goldilend.sol
251:   function boost(
252:     address[] calldata partnerNFTs,
253:     uint256[] calldata partnerNFTIds
254:   ) external {
255:     for(uint256 i; i < partnerNFTs.length; i++) {
256:       if(partnerNFTBoosts[partnerNFTs[i]] == 0) revert InvalidBoostNFT();
257:     }
258:     if(partnerNFTs.length != partnerNFTIds.length) revert ArrayMismatch();
259:     boosts[msg.sender] = _buildBoost(partnerNFTs, partnerNFTIds);
260:     for(uint8 i; i < partnerNFTs.length; i++) {
261:       IERC721(partnerNFTs[i]).safeTransferFrom(msg.sender, address(this), partnerNFTIds[i]);
262:     }
263:   }
```

\clearpage
