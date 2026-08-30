---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-23-cyfrin-sherpa-v2-0-0-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-11-23T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-23-cyfrin-sherpa-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-23-cyfrin-sherpa-v2-0
title: Owner can rescue the vault’s own share tokens
vuln_class: []
---

# Owner can rescue the vault’s own share tokens

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-23-cyfrin-sherpa-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-23-cyfrin-sherpa-v2.0.md)_

---

**Description:** [`SherpaVault::rescueTokens`](https://github.com/hedgemonyxyz/sherpa-vault-smartcontracts/blob/50eb8ad6ee048a767f7ed2265404c59592c098b7/contracts/SherpaVault.sol#L730-L740) forbids rescuing the wrapper token:
```solidity
// CRITICAL: Cannot rescue the wrapper token (user funds)
// This protects deposited SherpaUSD from being withdrawn by owner
if (token == stableWrapper) revert CannotRescueWrapperToken();
```

But it allows rescuing the vault’s own share token (`token == address(vault)`). Since[ newly minted shares](https://github.com/hedgemonyxyz/sherpa-vault-smartcontracts/blob/50eb8ad6ee048a767f7ed2265404c59592c098b7/contracts/SherpaVault.sol#L543-L544) for pending deposits are held in vault custody at `address(this)` and user redemptions transfer from this balance:
```solidity
accountingSupply += mintShares;
_mint(address(this), mintShares);
```

The owner can transfer out custody shares via `rescueTokens`, reducing the vault-held pool that backs users’ pending/redemption balances.

**Impact:** An owner (or compromised owner key) can move vault-custodied shares away from `address(this)`, which they then can withdraw for the underlying deposit.

**Recommended Mitigation:** Disallow rescuing the vault’s own share token:

```diff
- if (token == stableWrapper) revert CannotRescueWrapperToken();
+ if (token == stableWrapper || token == address(this)) revert CannotRescueWrapperToken();
```

**Sherpa:** Fixed in commit [`1a634e0`](https://github.com/hedgemonyxyz/sherpa-vault-smartcontracts/commit/1a634e0331968ea5a73f38a62ef824da9376ab52)

**Cyfrin:** Verified. The vault token is now also prevented from being rescued.
