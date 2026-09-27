---
affected_contracts: []
derives_from: []
id: solodit-codespect-2024-12-10-redstone-oracles-1-1
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2024-12-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2024-12-10-RedStone-Oracles.md
tags:
- firm:codespect
- report:2024-12-10-redstone-oracles
title: '[I-02] Unused Constant'
vuln_class: []
---

# [I-02] Unused Constant

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2024-12-10-RedStone-Oracles.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2024-12-10-RedStone-Oracles.md)_

---

**Original severity:** Best Practices

**Files:** [RedstoneConstants.sol](https://github.com/redstone-finance/redstone-oracles-monorepo/blob/ff0f3dcb085f28bd80ddc096825701db6e14d0af/packages/evm-connector/contracts/core/RedstoneConstants.sol#L21)

**Description:**

The `RedstoneConstants` contract defines various constants utilized across the `evm-connector` package. However, the constant `FUNCTION_SIGNATURE_BS` is not used in any contract.

Removing unused code is a best practice to maintain code clarity.

**Recommendation:** Consider the removal of the `FUNCTION_SIGNATURE_BS` constant.

**Status:** Fixed

**Client response:** Fixed in [be508fa80152bad5c8a4535a8ab1df18e4bad372](https://github.com/redstone-finance/redstone-oracles-monorepo/commit/be508fa80152bad5c8a4535a8ab1df18e4bad372).
