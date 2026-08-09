---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-2-5
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0
title: Use `SafeERC20` approval and transfer functions instead of standard IERC20
  functions for `liquidityToken`
vuln_class: []
---

# Use `SafeERC20` approval and transfer functions instead of standard IERC20 functions for `liquidityToken`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md)_

---

**Description:** The on-ramping and off-ramping processes are linked to external liquidity tokens such as stablecoins whose code is not controlled by the protocol; hence use [`SafeERC20::forceApprove, transfer, safeTransfer`](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/utils/SafeERC20.sol) when dealing with a range of potential tokens:
```solidity
on-ramp/provider/AllowanceAssetProvider.sol
98:        asset.transferFrom(assetProviderWallet, _buyer, _amount);

on-ramp/BaseOnRamp.sol
122:        liquidityToken.transferFrom(from, address(this), amount);
125:            liquidityToken.transfer(feeManager.feeCollector(), fee);
131:            liquidityToken.approve(address(USDCBridge), amountExcludingFee);
134:            liquidityToken.transfer(custodianWallet, amountExcludingFee);

off-ramp/provider/AllowanceLiquidityProvider.sol
141:        liquidityToken.transferFrom(liquidityProviderWallet, _redeemer, _liquidityAmount);

off-ramp/provider/CollateralLiquidityProvider.sol
186:        collateralToken.transferFrom(collateralProvider, address(this), collateralAmount);
189:        collateralToken.approve(address(externalCollateralRedemption), collateralAmount);
198:        liquidityToken.transfer(_redeemer, amountToSupply);

off-ramp/RedemptionManager.sol
43:            _params.asset.transferFrom(_params.redeemer, _params.liquidityProvider.recipient(), _params.assetAmount);
74:        _params.asset.transferFrom(_params.redeemer, _contractAddress, _params.assetAmount);
80:            _params.asset.transfer(_params.liquidityProvider.recipient(), _params.assetAmount);
96:        _params.liquidityProvider.liquidityToken().transfer(_params.redeemer, userSuppliedAmount);
100:            _params.liquidityProvider.liquidityToken().transfer(IFeeManager(_params.feeManager).feeCollector(), fee);
```

**Securitize:** Fixed in commit [a694dc3](https://github.com/securitize-io/bc-on-off-ramp-sc/commit/a694dc32386e038f8541ef79155b7a06a905fc52).

**Cyfrin:** Verified.
