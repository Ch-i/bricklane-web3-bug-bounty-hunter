---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-08-25-hyperwave-corewriter-0-1
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-08-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-08-25-Hyperwave-CoreWriter.md
tags:
- firm:codespect
- report:2025-08-25-hyperwave-corewriter
title: '[L-02] Joint withdrawal and spot transfer whitelist could lead to locked funds'
vuln_class: []
---

# [L-02] Joint withdrawal and spot transfer whitelist could lead to locked funds

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2025-08-25-Hyperwave-CoreWriter.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-08-25-Hyperwave-CoreWriter.md)_

---

**Files:** [`TradeStakeManager.sol`](https://github.com/SwellNetwork/hlp-corewriter/blob/5a19bb4373eaf3eb57d872f81d20177fb5cf9b2b/src/TradeStakeManager.sol#L618)

**Description:**

The `TradeStakeManager` contract uses `transferWhitelist` to validate both:

1. withdrawals from the account’s owned L1 address using `withdraw(...)` and `withdrawNative(...)`;
2. spot transfers using `spotSend(...)` and `spotSendUSDC(...)`;

This leads to a situation where a valid destination account used for `withdraw(...)` or `withdrawNative(...)` could be passed to the `spotSend(...)` or `spotSendUSDC(...)` and still be allowed. This could lead to transfer of the spot balance to an account which the protocol doesn’t have control of, and hence lead to locked funds. While this mistake would have to be made through an off-chain mechanism or the `BoringVault`, which is outside of the scope, it is worth raising the issue due to tight design control of the flow transfer within the protocol.

**Impact:** Potential loss of transferred funds.

**Recommendation:** Create separate whitelists for spot transfers and withdrawals

**Status:** Fixed

**Client response:** Resolved in [4b75b10a6aa5e1b59ed000bc7379af10eacefd67](https://github.com/SwellNetwork/hlp-corewriter/commit/4b75b10a6aa5e1b59ed000bc7379af10eacefd67)
