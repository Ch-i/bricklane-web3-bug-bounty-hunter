---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-25-planar-finance-1-4
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-03-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-25-Planar%20Finance.md
tags:
- firm:zokyo
- report:2024-03-25-planar-finance
title: Possibility of zero amount addition to staking positions
vuln_class: []
---

# Possibility of zero amount addition to staking positions

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-03-25-Planar Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-25-Planar%20Finance.md)_

---

**Severity**: Low

**Status**:  Unresolved

**Description**:

The `addToPosition` function within the `LpNFTPool` contract allows for the addition of positions with a zero amount due to the absence of a check after calling `_transferSupportingFeeOnTransfer`. This function is intended to add a specified amount to an existing staking position, provided the amount is greater than zero. However, if the token being staked has a transfer fee, the actual amount added to the staking position could be reduced to zero by the transfer mechanism, bypassing the initial non-zero check.

**Recommendation**: 

Consider moving the amount check after the token has been transferred.
