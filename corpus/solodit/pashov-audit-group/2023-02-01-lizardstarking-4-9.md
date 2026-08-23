---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-02-01-lizardstarking-4-9
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-02-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md
tags:
- firm:pashov-audit-group
- report:2023-02-01-lizardstarking
title: '[I-10] Variables can be turned into an `immutable` or a `constant`'
vuln_class: []
---

# [I-10] Variables can be turned into an `immutable` or a `constant`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-02-01-LizardStarking.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md)_

---

The `nominator` variable's value is known at compile-time so you can make it `private constant` as it is also not expected to be called outside of the contract, while the `Ethlizards`, `GenesisLiz` and `USDc` variables can be made `immutable` since they are only set in the constructor and never changed after that.
