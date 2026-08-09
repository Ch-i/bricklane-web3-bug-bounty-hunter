---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-17-cyfrin-stbl-ess-v2-0-3-6
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-06-17T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-17-cyfrin-stbl-ess-v2-0
title: '`STBL_YLD_SplitMerge::merge` is missing a `_tokenIdA != _tokenIdB` check'
vuln_class: []
---

# `STBL_YLD_SplitMerge::merge` is missing a `_tokenIdA != _tokenIdB` check

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-17-cyfrin-stbl-ess-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md)_

---

**Description:** `STBL_YLD_SplitMerge::merge` (`stbl-contracts-evm-redemptions/contracts/splitter/STBL_YLD_SplitMerge.sol:162-224`) accepts two token ids and validates ownership, disabled state, `assetID`, and `hairCut`, but never checks that the two ids are distinct:

```solidity
function merge(uint256 _tokenIdA, uint256 _tokenIdB) external whenNotPaused returns (uint256 newTokenId) {
    address caller = msg.sender;
    if (YLD.ownerOf(_tokenIdA) != caller) revert STBL_YLD_NotOwner(_tokenIdA);
    if (YLD.ownerOf(_tokenIdB) != caller) revert STBL_YLD_NotOwner(_tokenIdB);
    ...
    if (metaA.assetID != metaB.assetID) revert STBL_InvalidAsset(metaA.assetID, metaB.assetID);
    ...
}
```

When `_tokenIdA == _tokenIdB`, `merge` proceeds with both ids resolving to the same NFT, builds the merged metadata by summing every monetary field against itself, and then calls `YLD.burn` on that id twice. The second burn reverts inside `ownerOf` with `ERC721NonexistentToken` because the first burn already removed the token, so `merge` reverts with an opaque ERC-721 error rather than rejecting the invalid input up front.

The sibling `STBL_ESS_NFT_Vault1::_transferLot` performs exactly this distinct-operand check on its two parameters:

```solidity
if (_from == _to) revert STBL_ESS_InvalidTransfer(_from, _to);
```

`merge` has no equivalent guard on its two token-id parameters.

**Impact:** `merge(X, X)` reverts with a misleading `ERC721NonexistentToken` error instead of a clear domain-level rejection. No funds are at risk. Low.

**Recommended Mitigation:** Reject the equal-id case at the top of `merge`, matching the distinct-operand check `_transferLot` already uses:

```solidity
if (_tokenIdA == _tokenIdB) revert STBL_InvalidAsset(_tokenIdA, _tokenIdB);
```

**STBL:** Fixed in commits [7183df1](https://github.com/USD-Pi-Protocol/stbl-contracts-evm-redemptions/commit/7183df121a1f2503623fd12e1703cad38b333432) && [9315f68](https://github.com/USD-Pi-Protocol/stbl-contracts-evm-ess-common/commit/9315f68b79442e96f16d7ffc764c184d7a1f46a1).

**Cyfrin:** Verified. `STBL_YLD_SplitMerge` contracts now include a `_tokenIdA == _tokenIdB` guard at the top of merge
