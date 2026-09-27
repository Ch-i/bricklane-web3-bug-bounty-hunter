---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-07-02-hyperwave-sub-account-strategy-framework-0-1
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-07-02T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-07-02-Hyperwave-Sub-Account-Strategy-Framework.md
tags:
- firm:codespect
- report:2026-07-02-hyperwave-sub-account-strategy-framework
title: '[L-02] transferFundFromVault(...) uses unchecked transfer(...) call'
vuln_class: []
---

# [L-02] transferFundFromVault(...) uses unchecked transfer(...) call

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2026-07-02-Hyperwave-Sub-Account-Strategy-Framework.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-07-02-Hyperwave-Sub-Account-Strategy-Framework.md)_

---

**Files:** [SubAccountFundManager.sol](https://github.com/SwellNetwork/boring-vault/blob/6f6cd157b9aa4f63263e70339bbc37106cede493/src/base/Roles/SubAccountFundManager.sol)

**Description:**

`transferFundFromVault(...)` in `SubAccountFundManager.sol` moves the vault’s `baseAsset` to the calling strategy by encoding a raw `transfer(...)` call:

```solidity
boringVault.manage(
    address(baseAsset),
    abi.encodeWithSignature(
        "transfer(address,uint256)",
        msg.sender,
        amount
    ),
    0
);
```

The transfer call’s result is never checked. A token that returns `false` instead of reverting on failure would cause this call to succeed at the EVM level while no tokens actually move. Meanwhile, `allocated[msg.sender]` has already been incremented before this call is made, so the strategy’s allocation accounting would be updated even though the transfer silently failed.

**Impact:** Silent `transfer(...)` fails will cause accounting desync.

**Recommendation:** Check the `transfer(...)` call’s successful execution.

**Status:** Fixed

**Client response:** Fixed in [PR-87](https://github.com/SwellNetwork/boring-vault/pull/87).

**CODESPECT fix review:** Fixed in commit [`972021b`](https://github.com/SwellNetwork/boring-vault/commit/972021b25361f0d8f0cbe4e6fa50dfabc05275c5).
