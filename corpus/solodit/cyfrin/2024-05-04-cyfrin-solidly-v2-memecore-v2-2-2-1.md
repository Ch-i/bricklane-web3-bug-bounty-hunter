---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-04-cyfrin-solidly-v2-memecore-v2-2-2-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-05-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-04-cyfrin-solidly-v2-memecore-v2-2.md
tags:
- firm:cyfrin
- report:2024-05-04-cyfrin-solidly-v2-memecore-v2-2
title: Lack of events emitted for state changes
vuln_class: []
---

# Lack of events emitted for state changes

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-04-cyfrin-solidly-v2-memecore-v2-2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-04-cyfrin-solidly-v2-memecore-v2-2.md)_

---

**Description:** Events are useful to track contract changes off-chain. Hence emitting events for state changes is very valuable for off-chain monitoring and tracking of on-chain state.

**Impact:** Important state changes can be missed in monitoring and off chain tracing.

**Recommended Mitigation:** Consider emitting events for:
* `SolidlyV2Factory::setOwner`
* `SolidlyV2Factory::setFeeCollector`
* `SolidlyV2Factory::setFeeSetter`
* `SolidlyV2Pair::setCopilot`
* `SolidlyV2Pair::revokeFeeRole`

Also consider emitting a special event when tokens are burnt (but kept tracked for fee accrual):
* `SolidlyV2ERC42069::transferZero`
* `SolidlyV2ERC42069::transferZeroFrom`

**Solidly Labs:** Partially fixed. Most important events are covered, added `OwnerChanged` on factory. We're very constrained by bytecode space.

**Cyfrin:** Acknowledged.
