---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-04-25-tokentable-unlockerv2-evm-0-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-04-25T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-25-TokenTable-UnlockerV2-EVM.md
tags:
- firm:codespect
- report:2025-04-25-tokentable-unlockerv2-evm
title: '[M-01] Fixed fees allow users to transfer all the project tokens from the
  Unlocker to the protocol owner'
vuln_class: []
---

# [M-01] Fixed fees allow users to transfer all the project tokens from the Unlocker to the protocol owner

_Section severity (from Solodit section header): Medium_  
_Audit firm: CODESPECT_  
_Source report: [2025-04-25-TokenTable-UnlockerV2-EVM.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-25-TokenTable-UnlockerV2-EVM.md)_

---

**Files:** [TokenTableUnlockerV2.sol](https://github.com/EthSign/tokentable-v2-evm/tree/e27192f627ea849f88e8a4b68382c5ac8808e3a5/contracts/core/TokenTableUnlockerV2.sol)

**Description:**

In the `TTUFeeCollector` contract, protocol can set fixed fees for selected unlockers. These fees will get charged and transferred every time users call the `claim(...)` function. However, there is no minimum claim amount required for this function to complete. Users can call this function indefinitely until all the `ProjectTokens` in the `Unlocker` get transferred to the `TTUFeeCollector.owner()` as fees.

**Impact:** All the project tokens that have been deposited by the team to cover the users’ claims will be transferred to the Token Table protocol as fees.

**Recommendation:** For fixed fees there should be a reasonable minimum claiming amount.

**Status:** Fixed

**Update from TokenTable:** Fixed in [b119c645215fec35ae08aa2c431433ca52a3dce6](https://github.com/EthSign/tokentable-v2-evm/pull/11/commits/b119c645215fec35ae08aa2c431433ca52a3dce6)

**Update from CODESPECT:** The scenario involving a zero amount has been taken into account; however, in certain situations, the Fixed Fee may still exceed the amount being claimed.

**Update from TokenTable:** Acknowledged.
