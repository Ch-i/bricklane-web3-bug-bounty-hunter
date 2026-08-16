---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-22-cyfrin-doryoku-v2-0-2-5
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-07-22T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-22-cyfrin-doryoku-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-22-cyfrin-doryoku-v2-0
title: Redundant Instruction Attributes in `Initialize` and `Vest` Instructions
vuln_class: []
---

# Redundant Instruction Attributes in `Initialize` and `Vest` Instructions

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-22-cyfrin-doryoku-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-22-cyfrin-doryoku-v2.0.md)_

---

**Description:** In `xbelo` program's `Initialize` and `Vest` account structs, `#[instruction()]` and `#[instruction(amount: u64, vest_duration: i64)]` attributes are provided respectively.
This attribute declares instruction parameters that needs to be accessed during account validation.
Both of these can be safely removed since the first one declares no parameters and none are needed, and the latter one declares parameters(`amount` and `vest_duration`) that are not used in account validation constraints.

**Recommended Mitigation:** Consider removing `#[instruction(...)]` attributes from `Initialize` and `Vest` account structs since they are not necessary.

**Doryoku:**
Fixed in [41676f1](https://github.com/Warlands-Nft/xbelo/commit/41676f1ad0572f9b08fcd53c1d0a4a39b4fb9685).

**Cyfrin:** Verified.
