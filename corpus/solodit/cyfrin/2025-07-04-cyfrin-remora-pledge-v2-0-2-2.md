---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-2-2
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: '`TokenBank::addToken` should revert if token has already been added'
vuln_class: []
---

# `TokenBank::addToken` should revert if token has already been added

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** `TokenBank::addToken` should revert if token has already been added.

**Impact:** Token data such as `saleAmount` and `feeAmount` will be reset to zero causing other core functions to malfunction.

**Remora:** Fixed as of latest commit 2025/07/02 though exact commit unknown.

**Cyfrin:** Verified.
