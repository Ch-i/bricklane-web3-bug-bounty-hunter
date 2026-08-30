---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-28-cyfrin-rocko-refinance-v2-0-2-7
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-03-28T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-28-cyfrin-rocko-refinance-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-28-cyfrin-rocko-refinance-v2-0
title: Remove redundant `morphoMarketId` validation checks in `_closeLoanMorphoWithShares`
  and `_openLoanPosition`
vuln_class: []
---

# Remove redundant `morphoMarketId` validation checks in `_closeLoanMorphoWithShares` and `_openLoanPosition`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-28-cyfrin-rocko-refinance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-28-cyfrin-rocko-refinance-v2.0.md)_

---

**Description:** `RockoFlashRefinance::_closeLoanMorphoWithShares` and `_openLoanPosition` contain redundant validation `morphoMarketId`. The reasons why this validation is redundant:

* `RockoFlashRefinance::refinance` already validates the input `morphoMarketId`, encodes it into the `data` payload then calls `Morpho::flashLoan` with the `data` payload:
```solidity
if (_compareStrings(to, "morpho") || _compareStrings(from, "morpho")) {
    require(_isValidId(morphoMarketId), "Morpho Market ID required for Morpho refinance");
}

bytes memory data = abi.encode(
    rockoWallet,
    from,
    to,
    debtTokenAddress,
    collateralTokenAddress,
    aCollateralTokenAddress,
    morphoMarketId,
    morphoDebtShares
);

MORPHO.flashLoan(debtTokenAddress, debtBalance, data);
```

* `Morpho::flashLoan` always passes the unmodified `data` payload to `RockoFlashRefinance::onMorphoFlashLoan`:
```solidity
function flashLoan(address token, uint256 assets, bytes calldata data) external {
    require(assets != 0, ErrorsLib.ZERO_ASSETS);

    emit EventsLib.FlashLoan(msg.sender, token, assets);

    IERC20(token).safeTransfer(msg.sender, assets);

    // @audit passing unmodified `data` payload to `onMorphoFlashLoan`
    IMorphoFlashLoanCallback(msg.sender).onMorphoFlashLoan(assets, data);

    IERC20(token).safeTransferFrom(msg.sender, address(this), assets);
}
```

*`RockoFlashRefinance::onMorphoFlashLoan` decodes the unmodified `data` payload and calls `_closeLoanMorphoWithShares` and `_openLoanPosition` using the decoded `morphoMarketId` which has already been validated in `RockoFlashRefinance::refinance`.

**Recommended Mitigation:** Remove the redundant `morphoMarketId` validation checks at:
```solidity
325: require(_isValidId(morphoMarketId), "Invalid Morpho Market ID");

503: require(_isValidId(morphoMarketId), "Morpho Market ID required for Morpho refinance");
```

**Rocko:** Fixed in commit [5a9aa7d](https://github.com/getrocko/onchain/commit/5a9aa7d3cfb80150448608854440c285ea08fa53).

**Cyfrin:** Verified.
