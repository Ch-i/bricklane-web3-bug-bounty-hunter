---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-14-ondo-finance-0-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-06-14T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-14-Ondo%20Finance.md
tags:
- firm:zokyo
- report:2023-06-14-ondo-finance
title: Anyone can claim excess
vuln_class: []
---

# Anyone can claim excess

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2023-06-14-Ondo Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-14-Ondo%20Finance.md)_

---

**Severity**: High

**Status**: Resolved

**Description**

In the RWAHubNonStableInstantMints contract, there is no check for the msg.sender to be authorized to claim the excess of the deposit. The only check there is to be KYC'd. Therefore, anyone who went through the KYC could get a claim excess

**Recommendation**: 

add a check for the msg.sender to be authorized by the depositor.user to claim the excess or at least mint to the depositor user, not to msg.sender
