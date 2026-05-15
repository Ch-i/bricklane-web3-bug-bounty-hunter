---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-3-26
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-03-22T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md
tags:
- firm:recon-audits
- report:2025-03-22-apollon-report
title: '[L-27] `SwapPair` events use `msg.sender` but they should use the user taking
  on debt'
vuln_class: []
---

# [L-27] `SwapPair` events use `msg.sender` but they should use the user taking on debt

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Impact**

Events in SwapPair are logging `msg.sender` which will always be `swapOperations`

https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/SwapPair.sol#L125-L126

```solidity
    emit Mint(msg.sender, amount0, amount1); /// @audit QA: Mint should change to `to`

```

https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/SwapPair.sol#L169

```solidity
emit Burn(msg.sender, amount0, amount1, to); /// @audit QA: Mint should change to `to` or to the cdp Owner
```

**Mitigation**

Either change the log to `to` (the recipient), or add a `initiator` parameter and log that one

Alternatively, move the events in the `SwapOperations`
