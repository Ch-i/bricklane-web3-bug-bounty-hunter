---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-1-33
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Stale edge price in liquidation tree after perp withdraw call
vuln_class: []
---

# Stale edge price in liquidation tree after perp withdraw call

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** In `perp_withdraw`, after withdrawing funds from a perpetual position, the function does not call `change_edge_px` to update the liquidation price(edge price) in the liquidation tree.

When funds are withdrawn, `info.funds` decreases, which affects `total_funds` and consequently the edge price. However, the liquidation trees(`long_px` and `short_px`) continue to store the outdated edge price because `change_edge_px` is never invoked.

**Impact:** After a withdrawal, the liquidation trees retain stale edge prices because `change_edge_px` is never called. This leads to incorrect margin call detection and liquidation priority.


**Recommended Mitigation:** `change_edge_px` should be invoked for the user withdrawing funds at the end of the function.

**Deriverse:** Fixed in commit [4f7bc8](https://github.com/deriverse/protocol-v1/commit/4f7bc8ac68325aa93b339ff91c0ac794ea17ffd9).

**Cyfrin:** Verified.
