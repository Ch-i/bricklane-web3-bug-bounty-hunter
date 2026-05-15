---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-3-4
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-04-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md
tags:
- firm:cyfrin
- report:2024-04-06-cyfrin-beefy-finance
title: Use existing `available` function in `BeefyVaultConcLiq::balances`
vuln_class: []
---

# Use existing `available` function in `BeefyVaultConcLiq::balances`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-06-cyfrin-beefy-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md)_

---

**Description:** `BeefyVaultConcLiq` has an `available` function that [returns](https://github.com/beefyfinance/experiments/blob/14a313b76888581b05d42b6f7b6097c79f3e65c6/contracts/protocol/concliq/vault/BeefyVaultConcLiq.sol#L91-L94) the token balances held by the vault contract.

Refactor `balances` [L81-83](https://github.com/beefyfinance/experiments/blob/14a313b76888581b05d42b6f7b6097c79f3e65c6/contracts/protocol/concliq/vault/BeefyVaultConcLiq.sol#L81-L83) to use the existing `available` function to reduce code duplication and the possibility for errors creeping in when implementing the same functionality in multiple places.

One possible refactoring:
```solidity
(uint256 stratBal0, uint256 stratBal1) = IStrategyConcLiq(strategy).balances();
(uint256 vaultBal0, uint256 vaultBal1) = available();
return (stratBal0 + vaultBal0, stratBal1 + vaultBal1);
```

**Beefy:**
In commit [38ee643](https://github.com/beefyfinance/experiments/commit/38ee643ab661aba48f73b673ef2c8ed5ac63ed00) we removed the available function and exclude vault balances, as they are not accounted for in deposit or withdraw functions. They can be rescued by an owner function if for some reason someone sends tokens to the vault contract.
