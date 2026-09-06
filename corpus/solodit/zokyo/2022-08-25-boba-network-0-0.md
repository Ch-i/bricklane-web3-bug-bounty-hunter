---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-08-25-boba-network-0-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2022-08-25T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-08-25-Boba%20Network.md
tags:
- firm:zokyo
- report:2022-08-25-boba-network
title: Unchecked possible zero address for `_to` parameter in EthBridge.
vuln_class: []
---

# Unchecked possible zero address for `_to` parameter in EthBridge.

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2022-08-25-Boba Network.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-08-25-Boba%20Network.md)_

---

**Description**

In contract EthBridge.sol, at line 69 in function depositERC20To the_to function parameter can be zero and is not checked. The following function calls will not revert in case of a zero _to address, leading to undefined behavior, such as depositing tokens but not being able to receive them.
ftrace | funcSig
function depositERC20To(
69
address_l1Token
70
address _12Token,
71
address_tot,
72
uint256 _amount,
73
address_zroPaymentAddress
74
bytes memory _ adapterParams
75
bytes calldata_data
76
) external virtual payable {
77
require(_to != address(0), "EthBridge: zero_to address");
78
_initiateERC20Deposit(_l1Token
79
,
80
_12Token, msg.sender, _to

**Recommendation**

Add a sanity check for the_to address to not be zero and revert otherwise.

**Re-audit comment**

Resolved
