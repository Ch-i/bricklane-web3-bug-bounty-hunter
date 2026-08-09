---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-4-6
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-04-06T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md
tags:
- firm:cyfrin
- report:2024-04-06-cyfrin-beefy-finance
title: Avoid unnecessary initialization to zero in `BeefyVaultConcLiq::deposit`
vuln_class: []
---

# Avoid unnecessary initialization to zero in `BeefyVaultConcLiq::deposit`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-06-cyfrin-beefy-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md)_

---

**Description:** `BeefyVaultConcLiq::deposit` declares the `shares` variable on [L127](https://github.com/beefyfinance/experiments/blob/14a313b76888581b05d42b6f7b6097c79f3e65c6/contracts/protocol/concliq/vault/BeefyVaultConcLiq.sol#L157) initializing it to zero even though the `shares` variable is first used later in [L172](https://github.com/beefyfinance/experiments/blob/14a313b76888581b05d42b6f7b6097c79f3e65c6/contracts/protocol/concliq/vault/BeefyVaultConcLiq.sol#L172).

Avoid unnecessary initialization to zero by declaring and initializing `shares` at the same time in L172:
```solidity
uint256 shares = _amount1 + (_amount0 * price / PRECISION);
```

**Beefy:**
Fixed in commit [ea3aca8](https://github.com/beefyfinance/experiments/commit/ea3aca890816ea86f84ab721e6aa8993a591f061).

**Cyfrin:** Verified.
