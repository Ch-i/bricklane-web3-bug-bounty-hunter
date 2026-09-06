---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-05-18-bridgenetwork-1-2
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2022-05-18T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-05-18-BridgeNetwork.md
tags:
- firm:zokyo
- report:2022-05-18-bridgenetwork
title: In contract tokenLock.sol, function processedPayment, there’s a transferFrom
  call from a ERC20 contract without checking whether the call was succesful.
vuln_class: []
---

# In contract tokenLock.sol, function processedPayment, there’s a transferFrom call from a ERC20 contract without checking whether the call was succesful.

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2022-05-18-BridgeNetwork.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-05-18-BridgeNetwork.md)_

---

**Recommendation**:

Add SafeERC20 library in the contract and use safeTransferFrom instead of transferFrom to
make interactions with any tokens safe.
