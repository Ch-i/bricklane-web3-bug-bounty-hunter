---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-3-15
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-03-22T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md
tags:
- firm:recon-audits
- report:2025-03-22-apollon-report
title: '[L-16] Basic Style Guide advice'
vuln_class: []
---

# [L-16] Basic Style Guide advice

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Impact**

The impact from the current formatting is that manual review takes longer, and as such will be more expensive and error prone

**Specific Code Smells**

- Not using curly braces for `if / else`
- Using `ii` in favour of mathematical notation `n, l, m` `i, j, k`, `x, y, z`
- Breaking `CEI`
- Ping ponging of external calls
- Subtle changes against Liquity's version


**Breaking CEI**

`openTrove` shows an example of a seemingly innocuous way to break CEI

https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/BorrowerOperations.sol#L199-L224

```solidity
    vars.arrayIndex = contractsCache.troveManager.addTroveOwnerToArray(borrower);
    /// @audit move the transfer of coll to the bottom to avoid CEI issues
    // Move the coll to the active pool
    for (uint i = 0; i < vars.colls.length; i++) {
      TokenAmount memory collTokenAmount = vars.colls[i]; /// @audit CEI / Reentrancy
      _poolAddColl(
        borrower,
        contractsCache.storagePool,
        collTokenAmount.tokenAddress,
        collTokenAmount.amount,
        PoolType.Active
      );
    }
    /// @audit Where is the trove? 
    // Move the stable coin gas compensation to the Gas Pool
    contractsCache.storagePool.addValue(
      address(stableCoinAmount.debtToken),
      false,
      PoolType.GasCompensation,
      stableCoinAmount.netDebt
    ); /// @audit Not minting principal on open
    stableCoinAmount.debtToken.mint(address(contractsCache.storagePool), stableCoinAmount.netDebt);

    emit TroveCreated(borrower, _colls);
  }

```


With `_poolAddColl` looking as follows

https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/BorrowerOperations.sol#L840-L851

```solidity

  function _poolAddColl(
    address _borrower,
    IStoragePool _pool,
    address _collAddress,
    uint _amount,
    PoolType _poolType
  ) internal {
    _pool.addValue(_collAddress, true, _poolType, _amount);
    IERC20(_collAddress).transferFrom(_borrower, address(_pool), _amount); /// @audit FOT / SafeTransfer
  }

```

This would make it so that the system is recording the increase in collateral, but not the increase in debt, which would allow to drag the TCR below the Recovery Mode threshold, and liquidate all Troves that have a ICR < CCR

Liquity like systems tend to blur the idea of an external call as they effectively rely on external calls for accounting, but those can be viewed as trusted external calls

Whereas moving tokens should be viewed as an untrusted external call under the vast majority of circumnstances

You should refactor not to break CEI as it will:
- Ensure you cannot introduce exploits tied to ordering of external calls
- Make future review cheaper as CEI concerns will not take a considerable amount of time for review
