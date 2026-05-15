---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-17-cyfrin-octodefi-v2-0-0-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-07-17T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-17-cyfrin-octodefi-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-17-cyfrin-octodefi-v2-0
title: Missing access control on critical `FeeController` setters
vuln_class: []
---

# Missing access control on critical `FeeController` setters

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-17-cyfrin-octodefi-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-17-cyfrin-octodefi-v2.0.md)_

---

**Description:** `FeeController.setFunctionFeeConfig()`, `setTokenGetter()`, and `setGlobalTokenGetter()` are declared `external` but have **no modifier** restricting the caller. Any account can freely (re)configure fee percentages, token-getter addresses, or even swap in malicious contracts.

```solidity
/// @inheritdoc IFeeController
function setFunctionFeeConfig(bytes4 _selector, FeeType _feeType, uint256 _feePercentage) external {
    if (_feePercentage > maxFeeLimits[_feeType]) {
        revert FeePercentageExceedLimit();
    }

    functionFeeConfigs[_selector] = FeeConfig(_feeType, _feePercentage);

    emit FeeConfigSet(_selector, _feeType, _feePercentage);
}

/// @inheritdoc IFeeController
function setTokenGetter(bytes4 _selector, address _tokenGetter, address _target) external {
    if (_target == address(0) || _tokenGetter == address(0)) {
        revert ZeroAddressNotValid();
    }

    tokenGetters[_target][_selector] = _tokenGetter;
    emit TokenGetterSet(_target, _selector, _tokenGetter);
}

/// @inheritdoc IFeeController
function setGlobalTokenGetter(bytes4 _selector, address _tokenGetter) external {
    if (_tokenGetter == address(0)) {
        revert ZeroAddressNotValid();
    }

    globalTokenGetters[_selector] = _tokenGetter;
    emit GlobalTokenGetterSet(_selector, _tokenGetter);
}
```

**Impact:** Attackers can:
* Set the fee percentage to 0 and drain executors' revenue, or maximize it to grief smart accounts using the plugin.
* Cause DoS by setting the `tokenGetters` and `globalTokenGetters` to a contract that reverts on all calls


**Recommended Mitigation:** Add `onlyOwner` modifier to all state-changing admin setters inside `FeeController`.

**OctoDeFi:** Fixed in PR [\#12](https://github.com/octodefi/strategy-builder-plugin/pull/12).

**Cyfrin:** Verified. The `onlyOwner` modifier has been applied to the `setFunctionFeeConfig()`, `setTokenGetter()`, and `setGlobalTokenGetter()` functions.

\clearpage
