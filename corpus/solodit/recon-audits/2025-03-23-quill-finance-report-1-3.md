---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-quill-finance-report-1-3
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-quill-finance-report
title: '[L-04] Uncapped Caller Premium raises the likelihood of a unprofitable liquidation
  to SP stakers by a marginal amount'
vuln_class: []
---

# [L-04] Uncapped Caller Premium raises the likelihood of a unprofitable liquidation to SP stakers by a marginal amount

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Quill_Finance_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md)_

---

**Impact**

This change makes liquidations require an additional 50BPS to be able to pay the caller incentive
Overall this is not a massive change
And the change to a capped 5% premium for SP liquidation, paired with a lowest MCR of 110 makes this pretty safe overall as a choice

**Mitigation**

No mitigation is required at this time, you should monitor collaterals and raise the MCR if the current one causes bad debt redistributions or losses to the SP too frequently
