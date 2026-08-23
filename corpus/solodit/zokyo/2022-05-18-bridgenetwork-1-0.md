---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-05-18-bridgenetwork-1-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2022-05-18T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-05-18-BridgeNetwork.md
tags:
- firm:zokyo
- report:2022-05-18-bridgenetwork
title: In contract bridge.sol, functions send and burn do not implement the re-entrancy
  protection properly, you will think it is not necessary to specify the nonRenetrat
  modifier to the send and burn functions because those both functions calls t
vuln_class: []
---

# In contract bridge.sol, functions send and burn do not implement the re-entrancy protection properly, you will think it is not necessary to specify the nonRenetrat modifier to the send and burn functions because those both functions calls the deductFee function which have that protection active, but however before calling the deductFee function, there is another external call to the processedPayment function at line 423, here an malicious user, could create a token that will have a modified allowance function and with that will be possible to re-entar the send or burn functions, we are aware that the tokens addresses need to be pre-approved by an administrator but the malicious code could hide in plain sight and the malicious actor could use this technique to extract liquidity from his community using bridge.sol contract.

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2022-05-18-BridgeNetwork.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-05-18-BridgeNetwork.md)_

---

**Recommendation**:

Add the nonReentrant modifier to all the public/external functions that are doing external
calls or are changing the contract state and remove it from the internal/private functions, the
internal/private functions will be protected from re-entracy because the only way to call them
is through an public/external function anyway, so there is no need to add nonReentrant
modified on the private/internal function, but it is a strong need to add them on all the
external/public ones that are doing external calls or are changing the contract state.
