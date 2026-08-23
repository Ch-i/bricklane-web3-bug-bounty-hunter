---
affected_contracts: []
derives_from: []
id: solodit-auditone-2023-05-09-aurorafastbridge-3-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-05-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-05-09-Aurorafastbridge.md
tags:
- firm:auditone
- report:2023-05-09-aurorafastbridge
title: 'Unexpected token unlock could happen Severity: Quality Assurance'
vuln_class: []
---

# Unexpected token unlock could happen Severity: Quality Assurance

_Section severity (from Solodit section header): Informational_  
_Audit firm: AuditOne_  
_Source report: [2023-05-09-Aurorafastbridge.md](https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-05-09-Aurorafastbridge.md)_

---

**Description:**

As per docs, max of valid\_till or valid\_till\_block\_height is always taken to derive the unlock time: "valid\_till\_block\_height: Option — the same as valid\_till, but in block height, not in nanoseconds. If both values are provided, tokens will be locked on the max of the two values. (In that stage for User only None value makes sense)".

But seems like valid\_till\_block\_height is not actually used while checking valid time validity

As we can see in below function unlock time validation is only performed on valid\_till parameter and valid\_till\_block\_height param is not used.

**Recommendations:**

valid\_till\_block\_height should also be used to ![ref5]derive the unlock time.
