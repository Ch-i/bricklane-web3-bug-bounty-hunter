---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-3-22
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Redundant Flag `READY_TO_DRV_UPGRADE` Appears Unused
vuln_class: []
---

# Redundant Flag `READY_TO_DRV_UPGRADE` Appears Unused

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The `READY_TO_DRV_UPGRADE` flag appears to be redundant and potentially dead code. It is always set together with `READY_TO_PERP_UPGRADE`, but there is no separate DRV upgrade functionality in the codebase. The flag is never independently checked or used, suggesting it may be leftover code from a planned feature that was never implemented or was removed.
