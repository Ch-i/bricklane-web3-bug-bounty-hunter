---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-2-3
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
title: Not way to change the recipient in the liquidity provider in the offramp logic
vuln_class: []
---

# Not way to change the recipient in the liquidity provider in the offramp logic

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md)_

---

**Description:** Both` AllowanceLiquidityProvider` and `CollateralLiquidityProvider` contracts set the recipient address only during initialization, with no function to update it afterwards.
In `RedemptionManager.sol`, when` assetBurn` is false, tokens are transferred to the recipient:

```solidity
 if (_params.assetBurn) {
            _params.asset.burn(_params.redeemer, _params.assetAmount, "Redemption burn");
        } else {
            _params.asset.transferFrom(_params.redeemer, _params.liquidityProvider.recipient(), _params.assetAmount);//@audit not way to update the recipient?
        }
```

However, neither liquidity provider implements a setter for the recipient address. While both contracts provide setters for other addresses (`setAllowanceProviderWallet`, `setCollateralProvider`, `setExternalCollateralRedemption`), the recipient address cannot be modified after deployment.

**Impact:** If the recipient wallet is compromised, needs to change for operational reasons, or the receiving entity updates their wallet address, there is no way to update it without performing a full contract upgrade.

**Recommended Mitigation:** Add a `setRecipient` function to both `AllowanceLiquidityProvider` and `CollateralLiquidityProvider`.

**Securitize:** Acknowledged.
