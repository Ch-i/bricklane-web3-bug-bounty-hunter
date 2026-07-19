---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-10-13-thestandard-io-0-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2022-10-13T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-10-13-TheStandard.io.md
tags:
- firm:zokyo
- report:2022-10-13-thestandard-io
title: Lost assets if `collateralWallet` is zero address in SEuroOffering.
vuln_class: []
---

# Lost assets if `collateralWallet` is zero address in SEuroOffering.

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2022-10-13-TheStandard.io.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-10-13-TheStandard.io.md)_

---

**Description**

SEuroOffering.sol - body of transferCollateral(): As this method is triggered by an external call of swap and swapETH. An amount of an asset token is meant to be transferred to collateralWallet in exchange for SEuro.
if (collateralWallet != address(0))
token.transfer (collateralWallet, amount);
In case collateralWallet is zero-address token is not transferred to collateral wallet, hence token amount will be kept in balance of SEuroOffering contract. It is worth noting that the amount of token kept will be inaccessible. Hence, we end up having lost inaccessible assets. In biref: this leads to a scenario in which SEuroOffering can receive assets which are not going to be transferable. Assets shall not be accessible or controlled in this case, hence will be lost.

**Recommendation**

replace if by require.

**Re-audit comment**

Resolved
