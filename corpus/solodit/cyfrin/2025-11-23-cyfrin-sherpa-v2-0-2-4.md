---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-23-cyfrin-sherpa-v2-0-2-4
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-11-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-23-cyfrin-sherpa-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-23-cyfrin-sherpa-v2-0
title: Some SherpaUSD can never be unstaked due to minimumSupply check
vuln_class: []
---

# Some SherpaUSD can never be unstaked due to minimumSupply check

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-23-cyfrin-sherpa-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-23-cyfrin-sherpa-v2.0.md)_

---

**Description:** The `SherpaVault::_unstake` function in SherpaVault includes a check that ensures the total assets staked are never less than minimumSupply and greater than 0. However, it is possible for another user to intentionally or unintentionally block a user from unstaking permanently.

```solidity
// Ensure vault maintains minimum supply (allow full exit to 0)
        if (totalStaked - wrappedTokensToWithdraw < vaultParams.minimumSupply &&
            totalStaked - wrappedTokensToWithdraw > 0) {
            revert MinimumSupplyNotMet();
        }
```

For example:
 - Let's assume `minimumSupply` = 1000 SherpaUSD.
 - Alice deposits 1000 SherpaUSD.
 - Malicious Bob deposits 1 wei SherpaUSD. This is allowed since this if statement in function `_stakeInternal` -  `if (totalWithStakedAmount < _vaultParams.minimumSupply) revert MinimumSupplyNotMet();` checks the total staked supply + pending amount i.e. the totalWithStakedAmount, which is now 1000 SherpaUSD + 1 wei SherpaUSD.
 - Alice now cannot exit the system until Bob clears his withdrawal. This occurs due to the minimumSupply check in the `_unstake` function.
 - Alice can only withdraw 1 wei SherpaUSD while the remaining is permanently locked.

Based on the scripts shared, this issue does not pose a risk currently as `minimumSupply` is expected to be 1 USD.

**Recommended Mitigation:** It is recommended to implement either or both of the following recommendations as a safety measure:
1. Implement a setter function to keep the `minimumSupply` configurable.
2. Add check to ensure all users individually deposit above the minimum supply.

**Sherpa:** Fixed in commit [`720c2c0`](https://github.com/hedgemonyxyz/sherpa-vault-smartcontracts/commit/720c2c053d4e22fcb73a7bda97e4282fc749f5f4)

**Cyfrin:** Verified. A minimum deposit enforced. `minimumSupply` left immutable.
