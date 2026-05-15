---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-kleidi-report-0-10
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Kleidi_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-kleidi-report
title: '[L-11] `RecoverySpell` Comment only applies to benign spells'
vuln_class: []
---

# [L-11] `RecoverySpell` Comment only applies to benign spells

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Kleidi_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Kleidi_Report.md)_

---

**Impact**


The comment:

https://github.com/solidity-labs-io/kleidi/blob/1a06ac16bc99d0b4081281329d03064c3737f5e4/src/RecoverySpell.sol#L112-L117

```solidity
        /// no checks on parameters as all valid recovery spells are
        /// deployed from the factory which will not allow a recovery
        /// spell to be created that does not have valid parameters.
        /// A recovery spell can only be created by the factory if the Safe has
        /// already been created on the chain the RecoverySpell is being
        /// deployed on.
```

Only applies to benign spells

Malicious spells can be deployed anywhere by the compromised hot signer
