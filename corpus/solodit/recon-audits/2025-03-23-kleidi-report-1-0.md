---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-kleidi-report-1-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Kleidi_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-kleidi-report
title: '[G-01] `RecoverySpell` save gas by setting `recoveryInitiated = 0` to signify
  a Disabled Spell'
vuln_class: []
---

# [G-01] `RecoverySpell` save gas by setting `recoveryInitiated = 0` to signify a Disabled Spell

_Section severity (from Solodit section header): Gas_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Kleidi_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Kleidi_Report.md)_

---

**Gas - Set it to 0 to save gas due to refund**

https://github.com/solidity-labs-io/kleidi/blob/1a06ac16bc99d0b4081281329d03064c3737f5e4/src/RecoverySpell.sol#L302

```solidity
        recoveryInitiated = type(uint256).max;
```
There is no zero timestamp so this is a safe change
