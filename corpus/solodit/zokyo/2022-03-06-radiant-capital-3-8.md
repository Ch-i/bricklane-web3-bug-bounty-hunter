---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-06-radiant-capital-3-8
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2022-03-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md
tags:
- firm:zokyo
- report:2022-03-06-radiant-capital
title: 'User might have access to tokens, stored on contract''s balance. LockZap.sol:
  zapWETH().'
vuln_class: []
---

# User might have access to tokens, stored on contract's balance. LockZap.sol: zapWETH().

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-03-06-Radiant Capital.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md)_

---

**Description**

In case the user passes a parameter _from' equal to the address of LockZap.sol, WETH won't be transferred from msg.sender to address(this), and the contract will use WETH stored on LockZap's balance. The issue is marked as info, since the contract isn't supposed to store funds, however, such functionality should be verified. 

**Recommendation**: 

Verify that users should be able to pass 'from' as the address of LockZap.sol and use funds which could be stored on contract's balance. 

**Post-audit**: 

address(this) can't be passed when zapWETH is called() now.
