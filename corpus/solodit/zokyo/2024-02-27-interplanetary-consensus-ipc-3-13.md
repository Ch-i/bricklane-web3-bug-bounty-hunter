---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-02-27-interplanetary-consensus-ipc-3-13
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-02-27T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md
tags:
- firm:zokyo
- report:2024-02-27-interplanetary-consensus-ipc
title: Incorrect Comment In LibMaxPQ
vuln_class: []
---

# Incorrect Comment In LibMaxPQ

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-02-27-InterPlanetary Consensus (IPC).md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md)_

---

**Severity** - Informational

**Status** - Resolved

**Description**


The comment at L122 in LibMaxPQ says 
// parent power is not larger than that of the current child, heap condition met.

This is not true , it should be 

// parent power is not smaller than that of the current child, heap condition met.

This is because this is a max heap where parent value is larger than its child nodes.

 **Recommendation**: Correct the statements.
