---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-12-trzn-finance-0-4
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-01-12T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md
tags:
- firm:zokyo
- report:2024-01-12-trzn-finance
title: Risk Managers Are Not Paid Out In `Request_BuyETH`
vuln_class: []
---

# Risk Managers Are Not Paid Out In `Request_BuyETH`

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2024-01-12-TRZN Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md)_

---

**Severity** - High

**Status** - Resolved

**Description**

A user can request to buy ETH from the protocol in exchange with the stable tokens using the function Request_BuyETH in VaultETH_V2 . A portion of the ETH that should be sent to the user is reserved for the risk managers which is calculated at L380. 
After calculation of these amount the risk managers are not paid , just the amount to be transferred is calculated and stored into a local storage uint array.

**Recommendation**:

Add the transfers for the risk managers.
