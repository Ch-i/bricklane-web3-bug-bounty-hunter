---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-3-6
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-04-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md
tags:
- firm:cyfrin
- report:2024-04-06-cyfrin-beefy-finance
title: Use `Ownable2StepUpgradeable` instead of `OwnableUpgradeable`, `Ownable2Step`
  instead of `Ownable`
vuln_class: []
---

# Use `Ownable2StepUpgradeable` instead of `OwnableUpgradeable`, `Ownable2Step` instead of `Ownable`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-06-cyfrin-beefy-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md)_

---

**Description:** `StratFeeManagerInitializable` and `BeefyVaultConcLiq` should use `Ownable2StepUpgradeable` instead of `OwnableUpgradeable`.

`StrategyFactory` should use `Ownable2Step` instead of `Ownable`.

The 2-step ownable contracts are to be preferred for [safer](https://www.rareskills.io/post/openzeppelin-ownable2step) ownership transfers.

**Beefy:**
Acknowledged.
