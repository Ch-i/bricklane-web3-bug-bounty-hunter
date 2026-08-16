---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-kleidi-report-0-7
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Kleidi_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-kleidi-report
title: '[L-08] `Timelock` checks for `1` instead of `DONE_TIMESTAMP`'
vuln_class: []
---

# [L-08] `Timelock` checks for `1` instead of `DONE_TIMESTAMP`

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Kleidi_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Kleidi_Report.md)_

---

This should be `DONE_TIMESTAMP`

https://github.com/solidity-labs-io/kleidi/blob/1a06ac16bc99d0b4081281329d03064c3737f5e4/src/Timelock.sol#L430-L431

```solidity
        require(timestamp != 1, "Timelock: operation already executed");

```
