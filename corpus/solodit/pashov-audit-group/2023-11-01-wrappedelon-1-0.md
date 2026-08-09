---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-11-01-wrappedelon-1-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-11-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-11-01-WrappedElon.md
tags:
- firm:pashov-audit-group
- report:2023-11-01-wrappedelon
title: '[L-01] Disabling unwrapping will block all bridges at the same time'
vuln_class: []
---

# [L-01] Disabling unwrapping will block all bridges at the same time

_Section severity (from Solodit section header): Low_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-11-01-WrappedElon.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-11-01-WrappedElon.md)_

---

The `wrapEnabled` and `unwrapEnabled` variables are added as a mitigation mechanism against flawed bridges (that have potentially infinite mint vulnerability). The problem is that if this wrapped token is used by or integrated with multiple bridges, setting `unwrapEnabled` to `false` will block all bridges at the same time, even if just one of them is faulty. Consider switching to a mechanism that can handle multiple bridges integrations in a fault-tolerant way.
