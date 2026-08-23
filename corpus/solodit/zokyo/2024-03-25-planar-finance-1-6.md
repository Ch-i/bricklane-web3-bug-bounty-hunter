---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-25-planar-finance-1-6
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-03-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-25-Planar%20Finance.md
tags:
- firm:zokyo
- report:2024-03-25-planar-finance
title: Inaccuracy in the decimal assumption
vuln_class: []
---

# Inaccuracy in the decimal assumption

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-03-25-Planar Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-25-Planar%20Finance.md)_

---

**Severity**: Low

**Status**:  Unresolved

**Description**:

The Presale contract has a hardcoded constant, `MIN_TOTAL_RAISED_FOR_MAX_PLANE`, which assumes the usage of a stablecoin (USDC) with 6 decimals. This design choice introduces a vulnerability when the contract is deployed on blockchain networks where the stablecoin or sale token has a different decimal configuration. The discrepancy in decimal handling can lead to significant miscalculations in the token sale mechanics, potentially allowing tokens to be sold for far less than their intended price.

**Recommendation**: 

Consider dynamically adjusting the `MIN_TOTAL_RAISED_FOR_MAX_PLANE` value based on the decimal configuration of the sale token at the time of contract deployment.
