---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-quill-finance-report-3-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-quill-finance-report
title: '[I-03] Quill necessitates having borrow caps'
vuln_class: []
---

# [I-03] Quill necessitates having borrow caps

_Section severity (from Solodit section header): Informational_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Quill_Finance_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md)_

---

**Impact**

As discussed here #20 

Many assets on Scroll are extremely illiquid

This means that Quill cannot be fully trustless as some branches pose counter-party risk to all users

Because of this, it's necessary you add borrow caps as to limit the damage that borrowers can cause by borrowing with illiquid assets

**Mitigation**

Introduce borrow caps

You can set these up in the `BoldToken`
