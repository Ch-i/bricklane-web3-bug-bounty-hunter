---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-17-cyfrin-stbl-ess-v2-0-3-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-06-17T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-17-cyfrin-stbl-ess-v2-0
title: '`STBL_ESS_Wrapper1` initializer missing duplicate `assetID` check in `_ratios`
  causes double token pull and double NFT mint on every `ess_deposit`'
vuln_class: []
---

# `STBL_ESS_Wrapper1` initializer missing duplicate `assetID` check in `_ratios` causes double token pull and double NFT mint on every `ess_deposit`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-17-cyfrin-stbl-ess-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md)_

---

**Description:** `STBL_ESS_Wrapper1.__STBL_ESS_Wrapper1_init_unchained` configures the asset basket by iterating a caller-supplied `_ratios` array and appending each `_ratios[i].assetID` to the `assetIDs` storage array. The loop writes `Ratios[assetID]` per entry and then sets `assetIDs = ids` — where `ids` is allocated with length `_ratios.length`.

There is no check that each `assetID` is unique:
```solidity
uint256[] memory ids = new uint256[](_ratios.length);
for (uint256 i = 0; i < _ratios.length; i++) {
    Ratios[_ratios[i].assetID].ratio  = _ratios[i].ratio;
    Ratios[_ratios[i].assetID].issuer = AssetData.issuer;
    ...
    ids[i] = _ratios[i].assetID;
}
assetIDs = ids;
```

Both `iCalculateRatios` and `asset_issue` iterate `assetIDs.length` without deduplication. With a duplicate entry, `asset_issue` executes `IERC20.transferFrom` twice for the same asset token — pulling double the intended amount from the depositing user.

**Impact:** If `_ratios` contains the same `assetID` twice, `assetIDs` ends up with two entries for that ID. The `Ratios` mapping uses last-writer-wins so the final mapping value is consistent, but `assetIDs.length` is permanently inflated.

A secondary consequence exists in `STBL_XLayer_Wrapper.initialize`, which has a parallel loop (`assetTokens.push(_ratios[i].token)`) that also lacks deduplication. `ess_withdraw` iterates `assetTokens` to return balance deltas to the caller; a duplicate token address there causes the contract to transfer the same token's recovered balance twice to the withdrawer, potentially draining any residual token balance held by the wrapper.

**Recommended Mitigation:** In `__STBL_ESS_Wrapper1_init_unchained`, add a uniqueness check for each `assetID` before writing to the `Ratios` mapping. Because the mapping is zero-initialized, a non-zero `issuer` value after the first write is a reliable duplicate signal — revert with a custom error if `Ratios[_ratios[i].assetID].issuer != address(0)` at the start of each iteration.

Apply the same guard to the `assetTokens` loop in `STBL_XLayer_Wrapper.initialize`, or derive `assetTokens` from the already-validated `assetIDs` array after the parent initializer returns.

**STBL:** Fixed in commits [0a0832e](https://github.com/USD-Pi-Protocol/stbl-contracts-evm-ess-common/commit/0a0832ebabdda52df2f128c2ee89cff9b57fb581) & [0d77f23](https://github.com/USD-Pi-Protocol/stbl-contracts-evm-ess-common/commit/0d77f23b5401da79d8862647d1281e0402d59bdb).

**Cyfrin:** Verified. The abstract `STBL_ESS_Wrapper1` initializer now rejects duplicate `assetID` entries via two guards — a mapping check (`Ratios[assetID].issuer != address(0)`) and a loop over the already-populated ids array — both reverting with `STBL_ESS_DuplicateAssetID`.

The concrete `STBL_XLayer_Wrapper` eliminates the secondary issue entirely by removing the separate `assetTokens` array; `ess_withdraw` now derives token addresses directly from `Ratios[assetIDs[i]].token`, closing the double-transfer path that existed when a duplicate token address appeared twice in that list
