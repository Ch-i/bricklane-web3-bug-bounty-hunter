---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-01-16-nord-finance-0-3
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2021-01-16T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-01-16-Nord%20Finance.md
tags:
- firm:zokyo
- report:2021-01-16-nord-finance
title: VaultDAI, VaultUSDC, VaultUSDT, AaveStrategy, CompoundStrategy contracts are
  missing predefined list of addresses that can be used to verify correct initialization
  of them as they specifically have to be used with specific contracts.
vuln_class: []
---

# VaultDAI, VaultUSDC, VaultUSDT, AaveStrategy, CompoundStrategy contracts are missing predefined list of addresses that can be used to verify correct initialization of them as they specifically have to be used with specific contracts.

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2021-01-16-Nord Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-01-16-Nord%20Finance.md)_

---

**Recommendation**:

Define allowed list of contracts addresses with reference to chain id.
