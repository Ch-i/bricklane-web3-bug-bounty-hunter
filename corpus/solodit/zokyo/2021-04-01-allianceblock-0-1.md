---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-04-01-allianceblock-0-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2021-04-01T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-04-01-AllianceBlock.md
tags:
- firm:zokyo
- report:2021-04-01-allianceblock
title: ThrottledExit contract is affected by Out-of-gas error, because of usage of
  cycle to calculate nextAvailableExitBlock in case if current mined block is far
  in future comparing to initial nextAvailableExitBlock.
vuln_class: []
---

# ThrottledExit contract is affected by Out-of-gas error, because of usage of cycle to calculate nextAvailableExitBlock in case if current mined block is far in future comparing to initial nextAvailableExitBlock.

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2021-04-01-AllianceBlock.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-04-01-AllianceBlock.md)_

---

**Recommendation**:
Instead of doing iterations it is better to use mathematical formula to calculate
nextAvailableExitBlock as
```solidity
nextAvailableExitBlock = nextAvailableExitBlock + ((block.number - nextAvailableExitBlock) /
throttleRoundBlocks + 1) * throttleRoundBlocks
```
