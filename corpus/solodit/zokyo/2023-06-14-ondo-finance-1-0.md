---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-14-ondo-finance-1-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-06-14T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-14-Ondo%20Finance.md
tags:
- firm:zokyo
- report:2023-06-14-ondo-finance
title: Incorrect variable used to compare
vuln_class: []
---

# Incorrect variable used to compare

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2023-06-14-Ondo Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-14-Ondo%20Finance.md)_

---

**Severity**: Medium

**Status**: Resolved

**Description**

In the contract RWAHubOffChainRedemptions the function requestRedemptionServicedOffchain is using the `minimumRedemptionAmount` to compare the `amountRWATokenToRedeem` with while the `minimumOffChainRedemptionAmount` is unused

**Recommendation**: 

make sure `minimumOffChainRedemptionAmount` is needed
At the contract deployment the initial mints of the RWAHubNonStableInstantMints and RWAHubInstantMints are paused by default which may lead to excess call to `unpause` function before it actually starts working

inialize the instantMintPaused with false if mints need to be ready right after deployment
