---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-19-cyfrin-lido-earn-v2-0-1-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-12-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-19-cyfrin-lido-earn-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-19-cyfrin-lido-earn-v2-0
title: '`Vault::decimals` does not reflect correct decimals when `OFFSET` is used'
vuln_class: []
---

# `Vault::decimals` does not reflect correct decimals when `OFFSET` is used

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-19-cyfrin-lido-earn-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-19-cyfrin-lido-earn-v2.0.md)_

---

**Description:** [`Vault::decimals`](https://github.com/lidofinance/defi-interface/blob/99fd2b2c64c345a3c14b023dca4cb6393ffce5aa/src/Vault.sol#L543-L545) simply returns the asset decimals:
```solidity
function decimals() public view virtual override(ERC20, ERC4626) returns (uint8) {
    return IERC20Metadata(asset()).decimals();
}
```
This is different to the OpenZeppelin [ERC4626 implementation](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/extensions/ERC4626.sol#L129-L131), where they account for any decimal offset:
```solidity
function decimals() public view virtual override(IERC20Metadata, ERC20) returns (uint8) {
    return _underlyingDecimals + _decimalsOffset();
}
```

**Impact:** Although the issue will not cause any calculation errors it will cause the exchange rate and share tokens to look strange.

**Recommended Mitigation:** Consider replicating the OpenZeppelin implementation and adding the `OFFSET` to the decimals:
```diff
- return IERC20Metadata(asset()).decimals();
+ return IERC20Metadata(asset()).decimals(); + OFFSET;
```

**Lido:** FIxed in commit [`9ce9c0a`](https://github.com/lidofinance/defi-interface/commit/9ce9c0a5bef423933ec357ab3900d899069f2107)

**Cyfrin:** Verified. `OFFSET` is now added to the decimals.
