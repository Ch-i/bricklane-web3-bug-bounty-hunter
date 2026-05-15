---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-10-cyfrin-benqi-governance-v2-0-0-8
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-11-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-10-cyfrin-benqi-governance-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-10-cyfrin-benqi-governance-v2-0
title: Gauge removal before rewards distribution should be explicitly prevented to
  avoid erroneous loss of vote weight
vuln_class: []
---

# Gauge removal before rewards distribution should be explicitly prevented to avoid erroneous loss of vote weight

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-10-cyfrin-benqi-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-10-cyfrin-benqi-governance-v2.0.md)_

---

**Description:** Reward distributions occur following the conclusion of the voting period, in which Miles token holders allocate their voting power toward their choses gauge(s). However, if a gauge is removed after the voting period concludes but before the distribution phase begins, no rewards will be distributed for that gauge. Consequently, all votes cast for the removed gauge will be rendered obsolete.

**Impact:** All votes cast during the affected epoch for the removed gauge will be invalidated, leading to a total loss of voting weight and corresponding rewards for the voters.

**Recommended Mitigation:** `DistributionManager::_isEpochDistributed` determines whether an epoch has already been distributed. This check can be combined with the condition that voting has not yet started to create a new method within the `DistributionManager`. This new method can then be utilized within the `GaugeRegistrar` to ensure that gauges cannot be removed during this critical interval, preventing loss of user votes and ensuring proper reward distribution.

**BENQI:** Acknowledged. The solution to this is quite complex and not worth.

One way would be that we only allow unregistering gauge when time is between epoch start and voting start, but this would mean that if admin wants to remove gauge, he has to wait for a very specific time to be able to do so.

**Cyfrin:** Acknowledged.
