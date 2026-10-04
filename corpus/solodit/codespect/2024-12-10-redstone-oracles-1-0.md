---
affected_contracts: []
derives_from: []
id: solodit-codespect-2024-12-10-redstone-oracles-1-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2024-12-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2024-12-10-RedStone-Oracles.md
tags:
- firm:codespect
- report:2024-12-10-redstone-oracles
title: '[I-01] Compiler Version with Assembly Bugs'
vuln_class: []
---

# [I-01] Compiler Version with Assembly Bugs

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2024-12-10-RedStone-Oracles.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2024-12-10-RedStone-Oracles.md)_

---

**Original severity:** Best Practices

**Files:** [on-chain-relayer/*.sol](https://github.com/redstone-finance/redstone-oracles-monorepo/tree/ff0f3dcb085f28bd80ddc096825701db6e14d0af/packages/on-chain-relayer)

**Description:**

The the `on-chain-relayer` package rely on compiler version (`^0.8.14`) known to have bugs affecting assembly code blocks. While your current code does not appear to be impacted, it is strongly recommended to upgrade to the latest Solidity version or at least to `^0.8.15`, which addresses the bugs detailed [here](https://soliditylang.org/blog/2022/06/15/solidity-0.8.15-release-announcement/).

**Recommendation:** Upgrade the Solidity compiler to the latest version to ensure the integrity and security of the contracts.

**Status:** Fixed

**Client response:** Fixed in [198c17ee5123fbcc654b9490c8ea2d0857638705](https://github.com/redstone-finance/redstone-oracles-monorepo/commit/198c17ee5123fbcc654b9490c8ea2d0857638705)
