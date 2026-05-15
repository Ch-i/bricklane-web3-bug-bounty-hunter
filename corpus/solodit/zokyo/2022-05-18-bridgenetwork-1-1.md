---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-05-18-bridgenetwork-1-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2022-05-18T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-05-18-BridgeNetwork.md
tags:
- firm:zokyo
- report:2022-05-18-bridgenetwork
title: In contract bridge.sol, function processedPayment, line 424, is a call to the
  transferFrom function from a ERC20 contract, because the address of the token contract
  is a token with user input, this can lead to a malicious attack, not all th
vuln_class: []
---

# In contract bridge.sol, function processedPayment, line 424, is a call to the transferFrom function from a ERC20 contract, because the address of the token contract is a token with user input, this can lead to a malicious attack, not all the tokens have requires inside their transfer or transferFrom functions that will make them fail if something is not ok during execution because the ERC20 standard does not requires it and this is the reason why the transfer functions have a return true statement.

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2022-05-18-BridgeNetwork.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-05-18-BridgeNetwork.md)_

---

**Recommendation**:

Add SafeERC20 library in the contract and use safeTransferFrom instead of transferFrom to
make interactions with any tokens safe.
