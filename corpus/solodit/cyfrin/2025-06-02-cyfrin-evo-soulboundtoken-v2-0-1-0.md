---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-02-cyfrin-evo-soulboundtoken-v2-0-1-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-06-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-02-cyfrin-evo-soulboundtoken-v2.0.md
tags:
- firm:cyfrin
- report:2025-06-02-cyfrin-evo-soulboundtoken-v2-0
title: Prefer`Ownable2Step` instead of `Ownable`
vuln_class: []
---

# Prefer`Ownable2Step` instead of `Ownable`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-02-cyfrin-evo-soulboundtoken-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-02-cyfrin-evo-soulboundtoken-v2.0.md)_

---

**Description:** Prefer [Ownable2Step](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/access/Ownable2Step.sol) instead of `Ownable` for [safer ownership transfer](https://www.rareskills.io/post/openzeppelin-ownable2step).

**Evo:**
Fixed in commit [620120e](https://github.com/contractlevel/sbt/commit/620120ec5a85c3a2dbd1be52af4ee34fe946efbe).

**Cyfrin:** Verified.
