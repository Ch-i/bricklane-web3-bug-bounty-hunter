---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-07-02-hyperwave-sub-account-strategy-framework-0-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-07-02T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-07-02-Hyperwave-Sub-Account-Strategy-Framework.md
tags:
- firm:codespect
- report:2026-07-02-hyperwave-sub-account-strategy-framework
title: '[L-01] Repayment path reverts if a blocklist-capable baseAsset blocks the
  strategy or the vault'
vuln_class: []
---

# [L-01] Repayment path reverts if a blocklist-capable baseAsset blocks the strategy or the vault

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2026-07-02-Hyperwave-Sub-Account-Strategy-Framework.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-07-02-Hyperwave-Sub-Account-Strategy-Framework.md)_

---

**Files:** [SubAccountFundManager.sol](https://github.com/SwellNetwork/boring-vault/blob/6f6cd157b9aa4f63263e70339bbc37106cede493/src/base/Roles/SubAccountFundManager.sol)

**Description:**

`transferFundBackToVault(...)` repays only via `baseAsset.safeTransferFrom(msg.sender, address(boringVault), amount)`, with `baseAsset` and `boringVault` immutable and no alternative route.

**Impact:** If `baseAsset` is blocklist-capable (USDC is used in the aprimeUSD deployment scripts), a blocklist of the calling strategy or the `boringVault` recipient makes this transfer revert, so that strategy cannot repay and its `allocated` cannot be reduced. It needs the token issuer to blocklist a protocol-controlled address, is not attacker-triggerable, and freezes one strategy’s repayment.

**Recommendation:** Provide a governance-controlled alternative repayment route, or accept and document the blocklist risk of the chosen `baseAsset`.

**Status:** Fixed

**Client response:** Added comment in [PR-87](https://github.com/SwellNetwork/boring-vault/pull/87).

**CODESPECT fix review:** Fixed in commit [`f4ff022`](https://github.com/SwellNetwork/boring-vault/commit/f4ff022e972bb88e6045cb10fe9db71433792837).
