---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-24-satin-exchange-2-5
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-02-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md
tags:
- firm:trust-security
- report:2023-02-24-satin-exchange
title: TRST-L-6 Modifier onlyNewEpoch() does not ensure new epoch is reached
vuln_class: []
---

# TRST-L-6 Modifier onlyNewEpoch() does not ensure new epoch is reached

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-02-24-Satin.Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md)_

---

**Description:** 
The modifier `onlyNewEpoch()` ensures at least **DURATION** seconds passed since the last 
voting action, but does not ensure it’s a different epoch:
```solidity
    modifier onlyNewEpoch(uint _tokenId) {
        require((block.timestamp / DURATION) * DURATION > 
          lastVoted[_tokenId], "TOKEN_ALREADY_VOTED_THIS_EPOCH");
```
This can result in users being able to execute two voting actions in a single epoch, something 
the protocol is trying to avoid.

**Recommended mitigation:**
In both `vote()` and `reset()` set **lastVoted** to the current epoch timestamp, which can be 
obtained from the **activePeriod** variable in SatinMinter.sol, and in the `onlyNewEpoch()` 
modifier require the current **activePeriod** to be strictly greater than **lastVoted**.

**Team response:**
Fixed

**Mitigation Review:**
The issue has been resolved as suggested, the modifier `onlyNewEpoch()` now requires the 
current activePeriod to be strictly greater than lastVoted, and lastVoted is set to the current 
activePeriod when either `vote()` or `reset()` is called.
