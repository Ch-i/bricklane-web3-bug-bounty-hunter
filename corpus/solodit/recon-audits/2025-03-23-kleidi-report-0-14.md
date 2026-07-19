---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-kleidi-report-0-14
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Kleidi_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-kleidi-report
title: '[L-15] Admin Sidestep - `Guard.sol` DelegateCall is still possible via Modules'
vuln_class: []
---

# [L-15] Admin Sidestep - `Guard.sol` DelegateCall is still possible via Modules

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Kleidi_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Kleidi_Report.md)_

---

Delegatecall could still be performed by setting up modules

IMO this is fine, however, signers should be warned that adding a module could cause a full sidestep of the security guarantees of the project

The same can happen via a fallback handler
