---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-11-cyfrin-strata-v2-1-2-3
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-06-11T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md
tags:
- firm:cyfrin
- report:2025-06-11-cyfrin-strata-v2-1
title: Use `SafeERC20::forceApprove` instead of standard `IERC20::approve`
vuln_class: []
---

# Use `SafeERC20::forceApprove` instead of standard `IERC20::approve`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-11-cyfrin-strata-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md)_

---

**Description:** Use [`SafeERC20::forceApprove`](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/utils/SafeERC20.sol#L101-L108) when dealing with a range of potential tokens instead of standard `IERC20::approve`:
```solidity
predeposit/yUSDeDepositor.sol
58:        pUSDe.approve(address(yUSDe), amount);

predeposit/pUSDeVault.sol
178:        USDe.approve(address(sUSDe), USDeAssets);

predeposit/pUSDeDepositor.sol
86:            asset.approve(address(vault), amount);
98:        sUSDe.approve(address(pUSDe), amount);
110:        USDe.approve(address(pUSDe), amount);
122:        token.approve(swapInfo.router, amount);
```

**Strata:** Fixed in commit [f258bdc](https://github.com/Strata-Money/contracts/commit/f258bdcc49b87a2f8658b150bc3e3597a5187816).

**Cyfrin:** Verified.
