---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-3-21
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-03-22T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md
tags:
- firm:recon-audits
- report:2025-03-22-apollon-report
title: '[L-22] Incompatibility with tokens that charge a fee on transfer'
vuln_class: []
---

# [L-22] Incompatibility with tokens that charge a fee on transfer

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Impact**

The system stores balances in storage and then updates them

Some tokens will charge a fee on transfer

Meaning that `_amount` stored in the `StoragePool` will be higher than the actual balance received

https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/BorrowerOperations.sol#L841-L851

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

These types of tokens are pretty rare, but this is a very common finding that you should think about

**Mitigation**

Imo acknowledge this and make sure not to use these tokens
