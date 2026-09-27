---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-02-04-dutch-protocol-2-5
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-02-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md
tags:
- firm:codespect
- report:2026-02-04-dutch-protocol
title: '[L-06] The presale(...) function may be DoS'
vuln_class: []
---

# [L-06] The presale(...) function may be DoS

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2026-02-04-Dutch-Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md)_

---

**Files:** [`Presale.sol`](https://github.com/dutch-protocol/Protocol-Contracts/tree/cec8b243aa645fdbe80e05e613eca69542b62a2e/src/Presale.sol#L366)

**Description:**

The presale is expected to be the first DUTCH purchase transaction to prevent users from frontrunning and buying DUTCH at the lowest price for profit. Therefore, when presale calculating the expected DUTCH output, a supply of 0 is used as the starting point by default. To prevent DUTCH purchases before the presale, the project team needs to pause the system. However, during the process of unpausing the system and calling `performUpkeep(...)` to settle the presale, if a malicious actor frontruns by calling `settleWithETH` or making a purchase, causing the DUTCH supply to be nonzero. Then `performUpkeep(...)` could fail due to slippage control.

**Impact:** `performUpkeep(...)` may fail due to frontrunning, causing the presale funds to be locked.

**Recommendation:** It is recommended to add an `isPresaleEnd` field in `DUTCHBondingHook` and prohibit calls to `_beforeSwap` and `swapETHForDUTCH` while this field is false. The field would be set to true after `swapExactETHForDUTCH` is called.

**Status:** Fixed

**Client response:** Fixed in commit [03c6753d1d7677f2d16d4aaf0b33e7238256d4d1](https://github.com/dutch-protocol/Protocol-Contracts/commit/03c6753d1d7677f2d16d4aaf0b33e7238256d4d1)
