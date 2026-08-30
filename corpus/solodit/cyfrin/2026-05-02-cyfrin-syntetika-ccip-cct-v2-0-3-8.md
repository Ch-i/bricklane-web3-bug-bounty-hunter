---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-02-cyfrin-syntetika-ccip-cct-v2-0-3-8
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-05-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-02-cyfrin-syntetika-ccip-cct-v2-0
title: '`BlacklistableUpgradeable::__Blacklistable_init` callable publicly during
  initialization'
vuln_class: []
---

# `BlacklistableUpgradeable::__Blacklistable_init` callable publicly during initialization

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md)_

---

**Description:** The initializer is `public onlyInitializing` rather than `internal onlyInitializing`.

**Recommended Mitigation:** Change visibility to `internal`.

**Syntetika:** Fixed in commit [`d7840b3`](https://github.com/SyntetikaLabs/monorepo/commit/d7840b33ebb99f1db16ad80caf3e1b29625c0641)

**Cyfrin:** Verified.
