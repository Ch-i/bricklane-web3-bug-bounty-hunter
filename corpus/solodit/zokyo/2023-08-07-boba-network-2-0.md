---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-08-07-boba-network-2-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-08-07T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-08-07-Boba%20Network.md
tags:
- firm:zokyo
- report:2023-08-07-boba-network
title: Floating Pragma
vuln_class: []
---

# Floating Pragma

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-08-07-Boba Network.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-08-07-Boba%20Network.md)_

---

**Description**

Throughout the codebase, the contracts that are unlocked at version ^0.8.12, and they should always be deployed with the same compiler version. By locking the pragma to a specific version, contracts are not accidentally getting deployed by using an outdated version that can introduce unintended consequences.

**Recommendation**

Lock the compiler version to a specific. Known bugs are featured here.

**Re-audit comment**

Acknowledged.
Comment: The client acknowledges the finding, but did not make any changes.
