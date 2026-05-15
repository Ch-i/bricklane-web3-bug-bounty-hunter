---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-3-24
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
title: '[L-25] `SwapOperations` computes the swap fees without accounting for how
  fees will alter reserves'
vuln_class: []
---

# [L-25] `SwapOperations` computes the swap fees without accounting for how fees will alter reserves

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Impact**

At a broadstroke The formula to compute the post-swap reserves used by `getAmountsOut` and `getAmountsIn` is as follows:

```
uint(reserveA) * reserveB) / (reserveB + amtB),
```

However, the math is not accounting for fees that will be taken on each swap, meaning that the post-swap reserves will not match this amount


**Mitigation**

You should technically also account for the updated price post taking fees, as that will be the price that the next person will pay

I don't have sufficient time to fully explore this issue and I highly recommend you simulate swaps to determine if this can cause significant losses
