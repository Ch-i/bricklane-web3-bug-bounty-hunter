---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-15-cyfrin-earnm-dropbox-v2-0-4-10
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-08-15T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-15-cyfrin-earnm-dropbox-v2-0
title: Remove call to `_requireCallerIsContractOwner` from `DropBox::setDefaultRoyalty`
  and `setTokenRoyalty` since they already have the `onlyOwner` modifier
vuln_class: []
---

# Remove call to `_requireCallerIsContractOwner` from `DropBox::setDefaultRoyalty` and `setTokenRoyalty` since they already have the `onlyOwner` modifier

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-15-cyfrin-earnm-dropbox-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md)_

---

**Description:** Remove call to `_requireCallerIsContractOwner` from `DropBox::setDefaultRoyalty` and `setTokenRoyalty` since they already have the `onlyOwner` modifier:
```diff
function setDefaultRoyalty(address receiver, uint96 feeNumerator) external onlyOwner {
-  _requireCallerIsContractOwner();
  _setDefaultRoyalty(receiver, feeNumerator);
}

function setTokenRoyalty(uint256 tokenId, address receiver, uint96 feeNumerator) external onlyOwner {
-  _requireCallerIsContractOwner();
  _setTokenRoyalty(tokenId, receiver, feeNumerator);
}
```

**Mode:**
Fixed in commit [2939602](https://github.com/Earnft/dropbox-smart-contracts/commit/2939602b20ff093cb21f37b151aa7f5638e109a2).

**Cyfrin:** Verified.
