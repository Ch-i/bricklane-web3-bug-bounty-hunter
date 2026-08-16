---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-12-cyfrin-paladin-valkyrie-v2-0-4-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-03-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-12-cyfrin-paladin-valkyrie-v2-0
title: The updated version of `BaseHook` should be used
vuln_class: []
---

# The updated version of `BaseHook` should be used

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-12-cyfrin-paladin-valkyrie-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md)_

---

**Description:** The abstract `BaseHook` contract is [stated](https://github.com/PaladinFinance/Valkyrie/blob/6b97685d127c97bc369c0613943f45a547d89b18/src/hooks/base/BaseHook.sol#L14) to have been copied from the `uniswap/v4-periphery` repository; however, this version of the contract is outdated. The `onlyByManager` modifier is not necessary as the `onlyPoolManager` modifier can be used instead. Additionally, the commented out code can be removed.

**Recommended Mitigation:** Use the updated `BaseHook` contract, ideally as an import instead of copying the file.

**Paladin:** Acknowledged, but no changes => The version of `BaseHook` that was copied is indeed from a previous version in `uniswap/v4-periphery`, but we prefer this past version as it already handles all hook methods, and do not need to refactor the Valkyrie Hooks for all the methods to be internal. As long as the complete Hook respects the `IHook` interface, we consider it a valid base.

**Cyfrin:** Acknowledged.
