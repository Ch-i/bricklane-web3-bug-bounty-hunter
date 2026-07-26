---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-3-17
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-03-22T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md
tags:
- firm:recon-audits
- report:2025-03-22-apollon-report
title: '[L-18] WIP - Invariants'
vuln_class: []
---

# [L-18] WIP - Invariants

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Troves should never break the check `_debtTokenUsedAsCollRatio(contractsCache, vars) > MAX_DEBTS_AS_COLLATERAL`**

**There should be n Trove with 0 net debt in the Sorted Trove**

**At no time I can perform an operation, then update the oracle, and trigger recover mode**

**At no time, I should be able to open a Trove, and liquidate it in the same block**

**I should not be able to skip Bad Debt Redistributions**

**Trove Manager**

**Post accrual `getTroveColl` is == pre-accrual `getTroveWithdrawableColls`**

**Liquidation Operation**

**Liquidations should raise the TCR of the system, unless the liquidation is done on a Trove with Bad Debt**

**This line should never execute (as the logic above doesn't allow it)**

https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/LiquidationOperations.sol#L352-L353

```solidity
      if (collToLiquidate > rAmount.toLiquidate) collToLiquidate = rAmount.toLiquidate; // in case of IMCR > ICR, but the trove still gets liquidated because ICR < TCR in recovery mode

```
