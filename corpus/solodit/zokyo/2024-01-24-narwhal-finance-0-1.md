---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-24-narwhal-finance-0-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-01-24T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-24-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2024-01-24-narwhal-finance
title: Lack of incentives to liquidate small positions
vuln_class: []
---

# Lack of incentives to liquidate small positions

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2024-01-24-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-24-Narwhal%20Finance.md)_

---

**Severity**: High

**Status**: Resolved

**Description**

The protocol expects positions to be liquidated when their margin value falls below the liquidation threshold. Liquidators should be incentivized to carry out these liquidations. If there is no profit to be earned, no one will undertake the liquidation. However, if a user opens many positions with very low margins, and these become undercollateralized, the gas cost of liquidation may exceed the profits from liquidating these positions. This could result in bad debt remaining in the protocol.

**Recommendation**: 

Set a minimum position size to ensure that liquidations are profitable.
