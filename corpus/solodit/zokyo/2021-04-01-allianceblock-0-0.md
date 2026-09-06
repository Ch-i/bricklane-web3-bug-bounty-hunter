---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-04-01-allianceblock-0-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2021-04-01T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-04-01-AllianceBlock.md
tags:
- firm:zokyo
- report:2021-04-01-allianceblock
title: AbstractPoolsFactory contract owner can transfer staked tokens to any address
  by calling method withdrawLPRewards and passing argument lpTokenContract that refers
  staking token contract.
vuln_class: []
---

# AbstractPoolsFactory contract owner can transfer staked tokens to any address by calling method withdrawLPRewards and passing argument lpTokenContract that refers staking token contract.

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2021-04-01-AllianceBlock.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-04-01-AllianceBlock.md)_

---

Recommendation:
Forbid contract owner to transfer staked tokens to any address.
