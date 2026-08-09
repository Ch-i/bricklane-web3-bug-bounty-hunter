---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-kleidi-report-0-16
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Kleidi_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-kleidi-report
title: '[L-17] `ConfigurablePause.sol` some indexed parameters are not particularly
  useful'
vuln_class: []
---

# [L-17] `ConfigurablePause.sol` some indexed parameters are not particularly useful

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Kleidi_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Kleidi_Report.md)_

---

**Not sure it makes sense to index this**

https://github.com/solidity-labs-io/kleidi/blob/1a06ac16bc99d0b4081281329d03064c3737f5e4/src/ConfigurablePause.sol#L46-L47

```solidity
    event PauseTimeUpdated(uint256 indexed newPauseStartTime);

```

That would be helpful to find all events at a time, but that's a pretty niche thing to do


Same here

https://github.com/solidity-labs-io/kleidi/blob/1a06ac16bc99d0b4081281329d03064c3737f5e4/src/ConfigurablePause.sol#L51-L54

```solidity
    event PauseDurationUpdated(
        uint256 indexed oldPauseDuration, uint256 newPauseDuration
    );

```
