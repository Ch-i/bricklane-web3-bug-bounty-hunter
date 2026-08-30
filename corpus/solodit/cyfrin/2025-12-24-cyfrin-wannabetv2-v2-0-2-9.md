---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-wannabetv2-v2-0-2-9
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-wannabetv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-wannabetv2-v2-0
title: Unused error `IBet::InvalidAmount`
vuln_class: []
---

# Unused error `IBet::InvalidAmount`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-wannabetv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-wannabetv2-v2.0.md)_

---

**Description:** The custom error `InvalidAmount` is declared in `IBet` but never used anywhere in the implementation. Consider removing it or using it in the amount check it's intended to validate.

**WannaBet:** Fixed in commit [6bddf7f](https://github.com/gskril/wannabet-v2/commit/6bddf7fc0be929fd10ac731ef87cebba9f7ee686).

**Cyfrin:** Verified.
