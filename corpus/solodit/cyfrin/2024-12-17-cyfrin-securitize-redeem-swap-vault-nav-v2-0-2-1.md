---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2-0-2-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-12-17T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2-0
title: Insufficient storage gap in BaseSecuritizeSwap contract
vuln_class: []
---

# Insufficient storage gap in BaseSecuritizeSwap contract

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2.0.md)_

---

**Description:** The BaseSecuritizeSwap contract implements a storage gap of 40 slots (`uint256[40] __gap`), which doesn't follow OpenZeppelin's practice of reserving 50 storage slots in total for upgradeable contracts. This deviation from the standard could potentially cause storage collision issues in future upgrades.

```solidity
abstract contract BaseSecuritizeSwap is BaseDSContract, PausableUpgradeable {
    // ... other contract code ...
    uint256[40] __gap; // @audit-issue LOW -> uint256[43]
}
```

Below shows the current storage layout.
```
forge inspect BaseSecuritizeSwap storage --pretty
| Name                         | Type                             | Slot | Offset | Bytes | Contract                                                 |
|------------------------------|----------------------------------|------|--------|-------|----------------------------------------------------------|
| services                     | mapping(uint256 => address)      | 0    | 0      | 32    | BaseSecuritizeSwap |
| __gap                        | uint256[49]                      | 1    | 0      | 1568  | BaseSecuritizeSwap |
| dsToken                      | contract IDSToken                | 50   | 0      | 20    | BaseSecuritizeSwap |
| stableCoinToken              | contract IERC20                  | 51   | 0      | 20    | BaseSecuritizeSwap |
| erc20Token                   | contract IERC20                  | 52   | 0      | 20    | BaseSecuritizeSwap |
| collateralToken              | contract IERC20                  | 53   | 0      | 20    | BaseSecuritizeSwap |
| issuerWallet                 | address                          | 54   | 0      | 20    | BaseSecuritizeSwap |
| liquidityProviderWallet      | address                          | 55   | 0      | 20    | BaseSecuritizeSwap |
| externalCollateralRedemption | contract IRedemption             | 56   | 0      | 20    | BaseSecuritizeSwap |
| swapMode                     | enum BaseSecuritizeSwap.SwapMode | 56   | 20     | 1     | BaseSecuritizeSwap |
| __gap                        | uint256[40]                      | 57   | 0      | 1280  | BaseSecuritizeSwap |
```

The storage of `BaseSecuritizeSwap` starts from `dstoken` and we can see 7 slots are used before the `__gap` variable.
Following the OpenZeppelin's general practice, we should add 43 slots gap at the end.

**Recommended Mitigation:** Increase the storage gap to 43 slots to align with OpenZeppelin's best practices:
```diff
abstract contract BaseSecuritizeSwap is BaseDSContract, PausableUpgradeable {
--    uint256[40] __gap;
++    uint256[43] __gap;
}
```

**Securitize:** Fixed in commit [0c2a6e](https://bitbucket.org/securitize_dev/securitize-swap/commits/0c2a6e94cea7d4ee30ed8bd0386530f533959c04).

**Cyfrin:** Verified.
