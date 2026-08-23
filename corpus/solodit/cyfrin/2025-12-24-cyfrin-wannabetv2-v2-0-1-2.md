---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-wannabetv2-v2-0-1-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-wannabetv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-wannabetv2-v2-0
title: Salt used by `BetFactory::createBet` excludes important parameters preventing
  multiple bets with same timestamps between the same entities
vuln_class: []
---

# Salt used by `BetFactory::createBet` excludes important parameters preventing multiple bets with same timestamps between the same entities

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-wannabetv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-wannabetv2-v2.0.md)_

---

**Description:** Multiple entities (especially programs) may wish to "batch create" multiple bets between themselves that all have the same timestamps.

This is impossible since `BetFactory::createBet` will revert as the salt used is composed of `maker, taker, acceptBy, resolveBy` but doesn't incorporate other fields such as `asset`, `makerStake`, `takerStake` or `betCount`.

**Recommended Mitigation:** The simplest solution is to just add `betCount` to the salt, but this introduces potential DoS vector via front-running. However this DoS vector is unlikely since it costs the attacker significant gas as they have to deploy the new contract, even though there is no gain apart from the temporary DoS.

Another solution is to add `asset`, `makerStake`, `takerStake` to the salt.

**WannaBet:** Acknowledged.
