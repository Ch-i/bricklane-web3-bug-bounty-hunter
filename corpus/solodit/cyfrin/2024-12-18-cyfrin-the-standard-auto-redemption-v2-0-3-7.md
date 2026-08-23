---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-3-7
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-12-18T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-18-cyfrin-the-standard-auto-redemption-v2-0
title: Redemption of Hypervisor collateral can be suboptimal
vuln_class: []
---

# Redemption of Hypervisor collateral can be suboptimal

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md)_

---

**Description:** Consider a vault with `20% WBTC`, `40% WETH`, and `40% WBTC Hypervisor` collateral in USD terms that is to be the target of auto redemption. Under the current logic, the `WBTC Hypervisor` address will be received from the API response as the collateral token to be redeemed. The `_token` variable is then reassigned to whichever underlying token is stored in the `hypervisorCollaterals` mapping (either `WBTC` or `WETH`, but not both):

```solidity
address _hypervisor;
if (hypervisorCollaterals[_token] != address(0)) {
    _hypervisor = _token;
    _token = hypervisorCollaterals[_hypervisor];
}
IRedeemable(_smartVault).autoRedemption(
    _smartVault, quoter, _token, _collateralToUSDCPath, _USDsTargetAmount, _hypervisor
);
```

If the mapping is configured such that `WBTC` is returned, it will not be possible to execute the most optimal redemption. This is a limitation the current design which could be improved by passing both a collateral token and an optionally non-zero Hypervisor token address in the API response.

**The Standard DAO:** Fixed by commit [fd1fe84](https://github.com/the-standard/smart-vault/commit/fd1fe846a16729d217514bb601a672f52722a611).

**Cyfrin:** The response has been modified to include both collateral token and Hypervisor token addresses; however, they should be validated to correctly correspond to one another before being used.

**The Standard DAO:** Fixed by commit [7346460](https://github.com/the-standard/smart-vault/commit/73464606afd58886ecf8fdf6372b6058566400a5).

**Cyfrin:** Verified. The additional validation has been added to `AutoRedemption::validData`.

\clearpage
