---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-07-05-made-for-gamers-0-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2022-07-05T00:00:00Z'
related_swc: []
severity: Critical
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-07-05-Made%20for%20gamers.md
tags:
- firm:zokyo
- report:2022-07-05-made-for-gamers
title: Lock period can be avoided with other ERC777 functions.
vuln_class: []
---

# Lock period can be avoided with other ERC777 functions.

_Section severity (from Solodit section header): Critical_  
_Audit firm: Zokyo_  
_Source report: [2022-07-05-Made for gamers.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-07-05-Made%20for%20gamers.md)_

---

**Description**

Expo.sol. Contract overrides transfer functions, such as transfer(), send(), burn() in order to check lock period. However, there are few ERC777 standard functions which are not overridden and thus, can be used to avoid lock period on transfer. The following ERC777 functions perform transfer and burn and don't validate lock period: operatorSend(), operatorBurn(), transferFrom().

**Recommendation**

Override these functions as well to validate lock period in them.

**Re-audit comment**

Resolved.

Post-audit:

Internal functions_send() ans_burn() were overridden to check lock period.
