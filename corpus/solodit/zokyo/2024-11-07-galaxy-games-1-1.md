---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-11-07-galaxy-games-1-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-11-07T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-11-07-Galaxy%20Games.md
tags:
- firm:zokyo
- report:2024-11-07-galaxy-games
title: Floating pragma
vuln_class: []
---

# Floating pragma

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-11-07-Galaxy Games.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-11-07-Galaxy%20Games.md)_

---

**Severity** - Informational

**Status** - Resolved

**Description**

The contract uses pragma solidity ^0.8.27.
This may result in the contracts being deployed using the wrong pragma version, which is different from the one they were tested with.

**Recommendation** 

It is recommended to lock the pragma version.
