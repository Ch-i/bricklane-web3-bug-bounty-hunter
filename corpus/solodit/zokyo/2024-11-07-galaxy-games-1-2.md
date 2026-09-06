---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-11-07-galaxy-games-1-2
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-11-07T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-11-07-Galaxy%20Games.md
tags:
- firm:zokyo
- report:2024-11-07-galaxy-games
title: Duplicated zero address check
vuln_class: []
---

# Duplicated zero address check

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-11-07-Galaxy Games.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-11-07-Galaxy%20Games.md)_

---

**Severity** - Informational

**Status** - Resolved

**Description**

The constructor() has a zero address check for the _delegate variable passed.
However, _delegate value is already checked in the both Ownable and OAppCore contracts which the GalaxyGames contract inherits from.
(https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/access/Ownable.sol#L40
https://github.com/LayerZero-Labs/devtools/blob/main/packages/oapp-evm/contracts/oapp/OAppCore.sol#L29)

**Recommendation** 

It is recommended to remove the zero address check for the _delegate variable passed.
