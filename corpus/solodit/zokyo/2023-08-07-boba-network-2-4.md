---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-08-07-boba-network-2-4
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-08-07T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-08-07-Boba%20Network.md
tags:
- firm:zokyo
- report:2023-08-07-boba-network
title: Bridge Cannot Handle ERC-20 Fee on Transfer
vuln_class: []
---

# Bridge Cannot Handle ERC-20 Fee on Transfer

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-08-07-Boba Network.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-08-07-Boba%20Network.md)_

---

**Description**

In the contract Teleportation.sol is used to transfer funds from L1 to L2. The function `teleportAsset()` sends and emits tokens based on the input of _amount'. If a token had a fee attached on transfer the contract can expect potential unexpected consequences if the fee is not exempt for this contract.

**Recommendation**

We recommend checking the balance received by the contract before updating/or emitting a value that is potentially incorrect. This additional logic will allow fee on transfer tokens to be bridged across without users losing funds.

**Re-audit comment**

Resolved.
Comment: The client does not expect this to be an issue as they will not support fee on transfer tokens.
