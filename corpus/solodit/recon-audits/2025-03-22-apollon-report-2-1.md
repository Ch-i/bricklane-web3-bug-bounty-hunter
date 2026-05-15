---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-2-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-03-22T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md
tags:
- firm:recon-audits
- report:2025-03-22-apollon-report
title: '[M-02] `_exchangeRate` value validation looks incorrect'
vuln_class: []
---

# [M-02] `_exchangeRate` value validation looks incorrect

_Section severity (from Solodit section header): Medium_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Impact**

By definition a value for `_exchangeRate` should be within the bounds of `STOCK_SPLIT_PRECISION`

```solidity
    if (_exchangeRate >= -STOCK_SPLIT_PRECISION && _exchangeRate < STOCK_SPLIT_PRECISION) revert InvalidExchangeRate();
```


**Mitigation**

It's unclear if this is incorrect

Either way I highly recommend simplifying the logic for stock splits to allow the owner to set a scalar multiplier and a divisor, this makes the logic a lot simpler with no additional risks
