---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1-3-9
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-07-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1
title: Missing slippage protection in external collateral redemption call
vuln_class: []
---

# Missing slippage protection in external collateral redemption call

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md)_

---

**Description:** In `CollateralLiquidityProvider::supplyTo()`, the function calls `externalCollateralRedemption.redeem(collateralAmount, 0)` with `0` as the `minOutputAmount` parameter, providing no slippage protection for the external redemption transaction.
While this function is protected by the `onlySecuritizeRedemption` modifier and is intended to be called only by the `SecuritizeOffRamp` contract where slippage control is implemented at a higher level, it can lead to a potential problem if any other integration uses this function in future implementation.

**Recommended Mitigation:** Calculate an appropriate minimum output amount based on the expected liquidity amount and apply a reasonable slippage tolerance. Or consider modifying the function to accept a `minOutputAmount` parameter or calculate it based on the expected output:

**Securitize:** Acknowledged.

**Cyfrin:** Acknowledged.

\clearpage
