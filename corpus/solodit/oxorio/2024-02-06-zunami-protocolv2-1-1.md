---
affected_contracts: []
derives_from: []
id: solodit-oxorio-2024-02-06-zunami-protocolv2-1-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-02-06T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-02-06-Zunami%20ProtocolV2.md
tags:
- firm:oxorio
- report:2024-02-06-zunami-protocolv2
title: '[FIXED] Array out of bounds in `_setTokens` when deleting tokens in `ZunamiPool`'
vuln_class: []
---

# [FIXED] Array out of bounds in `_setTokens` when deleting tokens in `ZunamiPool`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Oxorio_  
_Source report: [2024-02-06-Zunami ProtocolV2.md](https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-02-06-Zunami%20ProtocolV2.md)_

---

##### Location
File | Location | Line
--- | --- | ---
[ZunamiPool.sol](https://github.com/ZunamiProtocol/ZunamiProtocolV2/tree/8bc108201bef8c4d341ecd3a29a3b1d975019cec/contracts/ZunamiPool.sol#L88 "/contracts/ZunamiPool.sol") | contract `ZunamiPool` > function `_setTokens` | 88

##### Description
In the `_setTokens` function of the `ZunamiPool` contract, there is a potential for an array out-of-bounds error when attempting to delete more tokens than were initially set.

The function operates by setting or removing tokens from the array across `POOL_ASSETS` iterations. Consider the following sequence:
- Initially, the `_setTokens` function sets the token count equal to `POOL_ASSETS`.
- Subsequently, a number of tokens equal to `POOL_ASSETS-3` is passed to `_setTokens`, resulting in the removal of three tokens from the `_tokens` array.
- If `_setTokens` is then called to set a token count of `POOL_ASSETS-2`, an array out-of-bounds error will occur in the `_tokens` array.

##### Recommendation
We recommend revising the token deletion logic in `_setTokens` to ensure it does not attempt to delete more elements than are present in the array.

##### Update
Fixed in commit [`9ffa8e1b6128d1ade8459a4e492cee669ed241a1`](https://github.com/ZunamiProtocol/ZunamiProtocolV2/tree/9ffa8e1b6128d1ade8459a4e492cee669ed241a1/).
