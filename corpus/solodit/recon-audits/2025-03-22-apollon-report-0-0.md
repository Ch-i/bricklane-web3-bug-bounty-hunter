---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-0-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-03-22T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md
tags:
- firm:recon-audits
- report:2025-03-22-apollon-report
title: '[H-01] `updateSystemSnapshots_excludeCollRemainder` lacks access control'
vuln_class: []
---

# [H-01] `updateSystemSnapshots_excludeCollRemainder` lacks access control

_Section severity (from Solodit section header): High_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Impact**

The function `updateSystemSnapshots_excludeCollRemainder` doesn't have access control meaning that stakes can be manipulated

I found this by running invariant tests, with the simple check that no call should ever succeed


```solidity
 => [call] CryticTester.troveManager_updateSystemSnapshots_excludeCollRemainder((address,uint256)[])([]) (addr=0xA647ff3c36cFab592509E13860ab8c4F28781a66, value=0, sender=0x0000000000000000000000000000000000030000)
         => [call] TroveManager.updateSystemSnapshots_excludeCollRemainder((address,uint256)[])([]) (addr=0x48E4F3f3daE11341ff2eDF60Af6857Ae08C871C5, value=0, sender=0xA647ff3c36cFab592509E13860ab8c4F28781a66)
                 => [event] SystemSnapshotsUpdated([], [])
                 => [return ()]
         => [event] Log("should never be possible")
         => [panic: assertion failed]
```

**Mitigation**

Add a check to ensure that the caller is LiquidationOperations
