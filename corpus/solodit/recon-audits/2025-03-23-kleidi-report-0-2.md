---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-kleidi-report-0-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Kleidi_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-kleidi-report
title: '[L-03] `Timelock` unnecessary call of `_setRoleAdmin`'
vuln_class: []
---

# [L-03] `Timelock` unnecessary call of `_setRoleAdmin`

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Kleidi_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Kleidi_Report.md)_

---

The call

https://github.com/solidity-labs-io/kleidi/blob/1a06ac16bc99d0b4081281329d03064c3737f5e4/src/Timelock.sol#L307-L308

```solidity
        /// set the admin of the hot signer role to the default admin role
        _setRoleAdmin(HOT_SIGNER_ROLE, DEFAULT_ADMIN_ROLE); /// @audit prob implict
```

Is unnecessary

Since DEFAULT_ADMIN_ROLE == 0x00

Meaning that it will be admin role by default
