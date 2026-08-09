---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-12-cyfrin-molecule-onchainlab-v2-0-3-7
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-05-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-12-cyfrin-molecule-onchainlab-v2-0
title: '`OclDerivationConfig::setFactory` missing one-shot guard, asymmetric with
  sister setters'
vuln_class: []
---

# `OclDerivationConfig::setFactory` missing one-shot guard, asymmetric with sister setters

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-12-cyfrin-molecule-onchainlab-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md)_

---

**Description:** Owner can rotate `factory` arbitrarily; rotating to a different address breaks `LabNFT::notifyIdentityCreated` (which gates on `msg.sender == config.factory()`) for the active factory until reverted. Three sister setters in scope all enforce the one-shot guard; only `setFactory` is missing it.

**Files:**

`src/core/OclDerivationConfig.sol:36-40`.

**Recommended Mitigation:** `if (factory != address(0)) revert FactoryAlreadySet();` at the top of `setFactory`.

**Molecule:** Fixed in commit [89c834c](https://github.com/moleculeprotocol/onchainlabs/commit/89c834c).

**Cyfrin:** Verified.
