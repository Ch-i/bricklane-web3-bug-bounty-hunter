---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-23-cyfrin-soneium-shibuya-v2-0-1-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-12-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-23-cyfrin-soneium-shibuya-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-23-cyfrin-soneium-shibuya-v2-0
title: Incorrect documentation for mint function
vuln_class: []
---

# Incorrect documentation for mint function

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-23-cyfrin-soneium-shibuya-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-23-cyfrin-soneium-shibuya-v2.0.md)_

---

**Description:** The `mint` function's documentation incorrectly states it "disallows burning from address(0)" when it should be "disallows minting to address(0)".

**Recommended Mitigation:** Update the documentation to correctly reflect the function's behavior

**Startale:** Fixed in PR [8](https://github.com/StartaleLabs/ccip-contracts-registration/pull/8).

**Cyfrin:** Verified.
