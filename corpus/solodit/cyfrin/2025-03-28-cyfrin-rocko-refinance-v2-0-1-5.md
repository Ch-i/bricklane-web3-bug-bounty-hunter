---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-28-cyfrin-rocko-refinance-v2-0-1-5
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-03-28T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-28-cyfrin-rocko-refinance-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-28-cyfrin-rocko-refinance-v2-0
title: In `_withdrawAaveCollateral` fetch `aTokenAddress` from Aave instead of receiving
  as input in `refinance` as passing it to morpho and back again
vuln_class: []
---

# In `_withdrawAaveCollateral` fetch `aTokenAddress` from Aave instead of receiving as input in `refinance` as passing it to morpho and back again

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-28-cyfrin-rocko-refinance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-28-cyfrin-rocko-refinance-v2.0.md)_

---

**Description:** Aave's `aTokenAddress` is only required when withdrawing collateral in `_withdrawAaveCollateral`, but currently it is:
* passed in as input to `refinance`
* has some validation performed on it
* encoded along with other data and sent to `Morpho::flashLoan`
* then Morpho passes it back when calling `onMorphoFlashLoan`
* where it is decoded again and passed around some more

Instead of all this, simply use Aave's API function [`IPool::getReserveData`](https://github.com/aave/aave-v3-core/blob/782f51917056a53a2c228701058a6c3fb233684a/contracts/interfaces/IPool.sol#L582) to get the correct `aTokenAddress` inside `_withdrawAaveCollateral` where it is required:
```solidity
    function _withdrawAaveCollateral(
        address collateralAddress,
        uint256 collateralBalance,
        address rockoWallet
    ) private {
        DataTypes.ReserveData memory reserveData = AAVE.getReserveData(collateralAddress);

        // Rocko Wallet needs to send aToken here after debt is paid off
        // Be sure that Rocko Wallet has approved this contract to spend aTokens for > `collateralBalance` tokens
        _pullTokensFromCallerWallet(reserveData.aTokenAddress, rockoWallet, collateralBalance);

        // function withdraw(address asset, uint256 amount, address to)
        AAVE.withdraw(collateralAddress, collateralBalance, FLASH_LOAN_CONTRACT);
    }
```

Fetching this parameter via Aave's API removes unnecessary code/validations also decreases the attack surface.

**Rocko:** Fixed in commit [d793f96](https://github.com/getrocko/onchain/commit/d793f960598240fa3eacdc6a4ec67d55dcfa2a75).

**Cyfrin:** Verified.
