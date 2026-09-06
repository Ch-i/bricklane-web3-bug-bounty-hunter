---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-01-19-lyra-finance-1-6
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-01-19T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md
tags:
- firm:trust-security
- report:2023-01-19-lyra-finance
title: TRST-M-7 attackers can delay or disrupt hedging activity by abusing mutual
  exclusion with updateCollateral()
vuln_class: []
---

# TRST-M-7 attackers can delay or disrupt hedging activity by abusing mutual exclusion with updateCollateral()

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-01-19-Lyra Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md)_

---

**Description:**
`hedgeDelta()` is the engine behind the PoolHedger.sol used to offset exposure.
 GMX increase / decrease position requests are performed in two steps to minimize slippage attacks. Firstly, 
users call `increasePositionRequest()`. Every short period (usually several seconds), GMX keeper 
will execute all requests in a batch. The PoolHedger deals with this pending state using the 
**pendingOrderKey** parameter. When it is not 0, it is the key received from the last GMX 
position request. When there is a pending action, `hedgeDelta()` as well as `updateCollateral()` 
cannot be called. The latter function is another permissionless entry point, which triggers the 
correction of the leverage ratio on GMX to the target. The issue stems from the fact there are 
no DOS-preventions put in place, which allow attackers to continually call `updateCollateral()` 
as soon as the previous request completes, keeping the Hedger ever busy perfecting the 
leverage ratio, albeit not hedging properly. If done for a long enough period, the impact is an 
increased insolvency risk for the protocol as it is not delta-neutral.

**Recommended mitigation:**
One option is to make sure the delta correction is significant for it to succeed, preventing the 
DOS. Another option is to refactor the code to have only one entry point. This will guarantee 
the prioritization of delta-neutrality over reaching the target leverage ratio.

**Team response:**
Fixed
