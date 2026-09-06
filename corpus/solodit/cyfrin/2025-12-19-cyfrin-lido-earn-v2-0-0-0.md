---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-19-cyfrin-lido-earn-v2-0-0-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-12-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-19-cyfrin-lido-earn-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-19-cyfrin-lido-earn-v2-0
title: '`ERC4626Adapter::maxMint` reverts for uncapped target vaults'
vuln_class: []
---

# `ERC4626Adapter::maxMint` reverts for uncapped target vaults

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-19-cyfrin-lido-earn-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-19-cyfrin-lido-earn-v2.0.md)_

---

**Description:** `ERC4626Adapter::maxMint` forwards `TARGET_VAULT.maxDeposit(address(this))` into `_convertToShares`:
```solidity
function maxMint(address /* user */ ) public view override returns (uint256) {
    if (paused() || emergencyMode) return 0;
    uint256 maxAssets = TARGET_VAULT.maxDeposit(address(this));
    return _convertToShares(maxAssets, Math.Rounding.Floor);
}
```
The [EIP-4626 standard for `maxMint`/`maxDeposit`](https://eips.ethereum.org/EIPS/eip-4626#maxdeposit) states that:
> MUST return `2 ** 256 - 1` if there is no limit on the maximum amount of assets that may be deposited.

Standard ERC4626 implementations (like OpenZeppelin’s), `maxDeposit` / `maxMint` therefore return `type(uint256).max` as a default. Passing this value into `_convertToShares` causes `Math.mulDiv` to overflow and revert, so `maxMint` itself reverts instead of returning a valid upper bound.

**Impact:** `ERC4626Adapter::maxMint` reverts for vaults without any cap which disagrees with the [EIP-4626 standard](https://eips.ethereum.org/EIPS/eip-4626#maxmint) that `maxMint` "MUST NOT revert.".

**Proof of Concept:** Add the following test to `ERC4626Adapter.MaxDeposit.t.sol`:
```solidity
function test_MaxMintReverts() public {
    vm.expectRevert(stdError.arithmeticError);
    vault.maxMint(alice);
}
```

**Recommended Mitigation:** Add a check for the “unbounded” result from the target vault and avoid feeding `type(uint256).max` into `_convertToShares`. For example:

```solidity
function maxMint(address /* user */ ) public view override returns (uint256) {
    if (paused() || emergencyMode) return 0;

    uint256 maxAssets = TARGET_VAULT.maxDeposit(address(this));
    if (maxAssets == type(uint256).max) {
        // Underlying vault is effectively uncapped: propagate this instead of converting
        return type(uint256).max;
    }

    return _convertToShares(maxAssets, Math.Rounding.Floor);
}
```

**Lido:** Fixed in commit [`af57eb5`](https://github.com/lidofinance/defi-interface/commit/af57eb5e85911976b76318d9a527319812fb3130)

**Cyfrin:** Verified. Suggested fix implemented.
