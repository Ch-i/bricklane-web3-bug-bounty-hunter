---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-09-13-cyfrin-the-standard-smart-vault-v2-0-4-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-09-13T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md
tags:
- firm:cyfrin
- report:2024-09-13-cyfrin-the-standard-smart-vault-v2-0
title: Unnecessary call to `SmartVaultV4::usdCollateral` when depositing/withdrawing
  collateral to/from yield positions
vuln_class: []
---

# Unnecessary call to `SmartVaultV4::usdCollateral` when depositing/withdrawing collateral to/from yield positions

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md)_

---

**Description:** When depositing/withdrawing collateral to/from yield positions in `SmartVaultV4`, the Smart Vault is validated to remain sufficiently collateralized and the collateral value is validated to have not dropped by more than 10%:

```solidity
if (undercollateralised() || significantCollateralDrop(_preDepositCollateral, usdCollateral())) revert Undercollateralised();
```

This logic calls [`SmartVaultV4::usdCollateral`](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultV4.sol#L105-L114) to obtain the value of the Smart Vault collateral; however, this is an expensive call that performs multiple loops over collateral tokens and is also invoked within [`SmartVaultV4::undercollateralised`](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultV4.sol#L142-L144):

```solidity
function undercollateralised() public view returns (bool) {
    return minted > maxMintable(usdCollateral());
}
```

**Recommended Mitigation:** Consider calling `usdCollateral()` only once after the deposit/withdrawal of collateral, then pass that value to `undercollaterlised()` and `significantCollateralDrop()`. The current implementation of `undercollateralised()` can be refactored into a public function that calls `usdCollateral()` and passes the result to an internal `_undercollateralised()` function that takes the collateral value as argument.

**The Standard DAO:** Fixed by commit [`3fdefc8`](https://github.com/the-standard/smart-vault/commit/3fdefc8d9b4f46aad33993a26ca5a04defdf740a).

**Cyfrin:** Verified, a private function has been introduced.
