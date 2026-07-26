---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-12-cyfrin-molecule-onchainlab-v2-0-3-5
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-05-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-12-cyfrin-molecule-onchainlab-v2-0
title: '`SelectorManager::_installSelector` overwrite=true skips `onUninstall` on
  displaced module'
vuln_class: []
---

# `SelectorManager::_installSelector` overwrite=true skips `onUninstall` on displaced module

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-12-cyfrin-molecule-onchainlab-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md)_

---

**Description:** When `installModule(MODULE_TYPE_FALLBACK, ...)` is called with `data.overwrite == true` and a fallback already exists for that selector, `_installSelector` overwrites without invoking `IModule::onUninstall` on the displaced module and without emitting `FallbackSelectorUninstalled`.

**Impact:** Off-chain indexers desync, and because `installModule` itself does not bump the marketplace `state` counter the rewire is invisible to a buyer comparing pre-listing and post-listing state values.

**Files:**

`src/core/SelectorManager.sol:55-82`, `src/OnChainLab.sol:380-403`.

**Recommended Mitigation:** When `overwrite == true && ss.module != address(0)`, call `_clearSelectorData(selector)` first (capturing prior module + emitting uninstall event), then optionally `ModuleLib.uninstallModule(prev, "")` for SINGLE callType modules. Optionally remove the user-controlled `overwrite` flag entirely and require explicit `uninstallModule` first.

**Molecule:** Fixed in commit [3b4cb98](https://github.com/moleculeprotocol/onchainlabs/commit/3b4cb98).

**Cyfrin:** Verified.
