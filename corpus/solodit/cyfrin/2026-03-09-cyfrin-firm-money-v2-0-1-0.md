---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-09-cyfrin-firm-money-v2-0-1-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2026-03-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-09-cyfrin-firm-money-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-09-cyfrin-firm-money-v2-0
title: Imported constants remain unused
vuln_class: []
---

# Imported constants remain unused

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-09-cyfrin-firm-money-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-09-cyfrin-firm-money-v2.0.md)_

---

**Description:** The deployment script hardcodes `DEBT_LIMIT` values for the WETH and wstETH branches as `100_000_000e18` instead of using the `DEBT_LIMIT_ETH` and `DEBT_LIMIT_WSTETH` constants already imported from `Constants.sol`. The SNT, LINEA, and sGUSD branches omit `DEBT_LIMIT` entirely despite `DEBT_LIMIT_SNT`, `DEBT_LIMIT_LINEA`, and `DEBT_LIMIT_SGUSD` being imported.

**Impact:** If the debt limit constants in `Constants.sol` are updated, the deployment script will deploy with stale values for WETH/wstETH branches and missing values for the new collateral branches, leading to misconfigured `AddressesRegistry` contracts.

https://github.com/firm-money/firm/blob/main/contracts/script/DeployLiquity2.s.sol#L25-L26

```solidity
import {
  ...
  DEBT_LIMIT_ETH, DEBT_LIMIT_WSTETH, DEBT_LIMIT_RETH,
  DEBT_LIMIT_SNT, DEBT_LIMIT_LINEA, DEBT_LIMIT_SGUSD
} from "src/Dependencies/Constants.sol";`
```

https://github.com/firm-money/firm/blob/main/contracts/script/DeployLiquity2.s.sol#L368-L421

```solidity
// WETH
troveManagerParamsArray[0] = TroveManagerParams({
    ...
    DEBT_LIMIT: 100_000_000e18 // @audit should use DEBT_LIMIT_ETH
});

// wstETH
troveManagerParamsArray[1] = TroveManagerParams({
    ...
    DEBT_LIMIT: 100_000_000e18 // @audit should use DEBT_LIMIT_WSTETH
});

// SNT
troveManagerParamsArray[3] = TroveManagerParams({
    ...
    // @audit missing DEBT_LIMIT: DEBT_LIMIT_SNT
});
```

**Recommended Mitigation:** Use the imported constants for all branches:

```diff
- DEBT_LIMIT: 100_000_000e18 // $100M
+ DEBT_LIMIT: DEBT_LIMIT_ETH
```

And add the missing `DEBT_LIMIT` field for SNT, LINEA, and sGUSD using `DEBT_LIMIT_SNT`, `DEBT_LIMIT_LINEA`, and `DEBT_LIMIT_SGUSD` respectively.

**Firm Money:**
Fixed in commit [59e4a8a](https://github.com/firm-money/firm/pull/21/changes/59e4a8ae721e269f2646aa71316b202d57ba7b49).

**Cyfrin:** Verified.
