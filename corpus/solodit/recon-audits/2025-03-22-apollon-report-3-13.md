---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-3-13
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-03-22T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md
tags:
- firm:recon-audits
- report:2025-03-22-apollon-report
title: '[L-14] `claimUnassigned` may result in a slight difference between debt and
  coll percentages being claimed due to rounding errors'
vuln_class: []
---

# [L-14] `claimUnassigned` may result in a slight difference between debt and coll percentages being claimed due to rounding errors

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Impact**

Slight difference in debt and coll claimed due to rounding error

May be abused to get free coll due to coll rounding up to a unit or more and debts rounding down to 0

https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/BorrowerOperations.sol#L630-L637

```solidity
    DebtTokenAmount[] memory debtsToAdd = new DebtTokenAmount[](vars.priceCache.debtPrices.length);
    for (uint i = 0; i < vars.priceCache.debtPrices.length; i++) {
      address debtToken = vars.priceCache.debtPrices[i].tokenAddress;

      uint unassignedDebt = contractsCache.storagePool.getValue(debtToken, false, PoolType.Unassigned);
      if (unassignedDebt == 0) continue;

      uint toClaim = (unassignedDebt * _percentage) / DECIMAL_PRECISION;
```

**Mitigation**

You may want to at least require that if collateral is 1, then debt is at least 1 as well

You could also add explicit rounding up of debt, and rounding down of collateral

Please keep in mind that this could introduce more bugs so this is a delicate change
