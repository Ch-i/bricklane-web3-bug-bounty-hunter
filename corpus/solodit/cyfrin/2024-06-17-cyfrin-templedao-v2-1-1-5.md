---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-06-17-cyfrin-templedao-v2-1-1-5
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-06-17T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-06-17-cyfrin-templedao-v2.1.md
tags:
- firm:cyfrin
- report:2024-06-17-cyfrin-templedao-v2-1
title: Incorrect end time setting for spice auction
vuln_class: []
---

# Incorrect end time setting for spice auction

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-06-17-cyfrin-templedao-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-06-17-cyfrin-templedao-v2.1.md)_

---

**Description:** In `startAuction` function of `SpiceAuction` contract, the end time is set wrong.
```solidity
uint128 startTime = info.startTime = uint128(block.timestamp) + config.startCooldown;
uint128 endTime = info.endTime = uint128(block.timestamp) + config.duration;
```
Currently, `endTime` is set using `block.timestamp`, not `startTime` calculated above.

**Impact:** The auction end time becomes shorter than expected.

**Recommended Mitigation:** `endTime` should be calculated using `startTime` and `duration`
```solidity
uint128 endTime = info.endTime = startTime + config.duration;
```

**TempleDAO:** Fixed in [PR 1032](https://github.com/TempleDAO/temple/pull/1032)

**Cyfrin:** Verified
