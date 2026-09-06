---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-11-cyfrin-strata-v2-1-4-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-06-11T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md
tags:
- firm:cyfrin
- report:2025-06-11-cyfrin-strata-v2-1
title: Cache identical storage reads
vuln_class: []
---

# Cache identical storage reads

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-11-cyfrin-strata-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md)_

---

**Description:** As reading from storage is expensive, it is more gas-efficient to cache values and read them from the cache if the storage has not changed. Cache identical storage reads:

`PreDepositPhaser.sol`:
```solidity
// use PreDepositPhase.YieldPhase instead
19:        emit PhaseStarted(currentPhase);
```

`pUSDeDepositor.sol`:
```solidity
// cache sUSDe and pUSDe to save 3 storage reads
// also change `deposit` to cache `sUSDe` and pass it as input to `deposit_sUSDe` saves 1 more storage read
96:            SafeERC20.safeTransferFrom(sUSDe, from, address(this), amount);
98:        sUSDe.approve(address(pUSDe), amount);
99:        return IMetaVault(address(pUSDe)).deposit(address(sUSDe), amount, receiver);

// cache USDe and pUSDe to save 2 storage reads
// also change `deposit` to cache `USDe` and pass it as input to `deposit_USDe` saves 1 more storage read
107:            SafeERC20.safeTransferFrom(USDe, from, address(this), amount);
110:        USDe.approve(address(pUSDe), amount);
111:        return pUSDe.deposit(amount, receiver);

// cache USDe to save 2 storage reads
// also change `deposit` to cache `USDe` and `autoSwaps[address(asset)]` then pass them as inputs to `deposit_viaSwap` saves 2 more storage reads
127:        uint256 USDeBalance = USDe.balanceOf(address(this));
130:            tokenOut: address(USDe),
140:        uint256 amountOut = USDe.balanceOf(address(this)) - USDeBalance;
```

`yUSDeDepositor.sol`:
```solidity
// cache pUSDe and yUSDe to save 2 storage reads
56:            SafeERC20.safeTransferFrom(pUSDe, from, address(this), amount);
58:        pUSDe.approve(address(yUSDe), amount);
59:        return yUSDe.deposit(amount, receiver);
```

`MetaVault.sol`:
```solidity
// cache assetsArr.length
241:        for (uint i = 0; i < assetsArr.length; i++) {
```

**Strata:** Fixed in commit [9a19939](https://github.com/Strata-Money/contracts/commit/9a1993975912fbcbaf684811b25de229947671c9).

**Cyfrin:** Verified.
