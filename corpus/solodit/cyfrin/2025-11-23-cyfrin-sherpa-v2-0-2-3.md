---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-23-cyfrin-sherpa-v2-0-2-3
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-11-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-23-cyfrin-sherpa-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-23-cyfrin-sherpa-v2-0
title: '`SherpaVault::redeem` naming ambiguous'
vuln_class: []
---

# `SherpaVault::redeem` naming ambiguous

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-23-cyfrin-sherpa-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-23-cyfrin-sherpa-v2.0.md)_

---

**Description:** `SherpaVault` uses ERC-4626-adjacent terminology but different semantics. In ERC-4626, `redeem` means burning shares to withdraw assets. In `SherpaVault`, `redeem` means finalize a prior deposit by moving unredeemed shares into the user’s wallet. This naming can mislead integrators and tooling that assume ERC-4626 behavior.

Consider renaming `redeem` to `finalizeDeposit` / `claimShares` to prevent confusion.

**Sherpa:** Fixed in commit [`8e9ba92`](https://github.com/hedgemonyxyz/sherpa-vault-smartcontracts/commit/8e9ba923e8402b877e16cd1d9a89143acdafe855)

**Cyfrin:** Verified. `claimShares` now used.
