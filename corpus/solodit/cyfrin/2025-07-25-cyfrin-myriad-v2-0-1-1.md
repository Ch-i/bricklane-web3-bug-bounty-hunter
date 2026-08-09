---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-25-cyfrin-myriad-v2-0-1-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-07-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-25-cyfrin-myriad-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-25-cyfrin-myriad-v2-0
title: Consider Using `Ownable2StepUpgradeable`
vuln_class: []
---

# Consider Using `Ownable2StepUpgradeable`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-25-cyfrin-myriad-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-25-cyfrin-myriad-v2.0.md)_

---

**Description:** The contracts currently use `OwnableUpgradeable` for access control. To improve safety, consider upgrading to `Ownable2StepUpgradeable`, which enforces an explicit acceptance step for ownership transfers and helps prevent accidental loss of control.

Consider replacing `OwnableUpgradeable` with `Ownable2StepUpgradeable` to enforce a two-step transfer pattern.

In addition, consider overriding the `renounceOwnership()` function to always revert. This prevents accidental or unintended renouncement of ownership, which can leave the contract permanently without an authorized admin.

**Myriad:** Fixed in [PR#83](https://github.com/Polkamarkets/polkamarkets-js/pull/83), commit [`8efe6e4`](https://github.com/Polkamarkets/polkamarkets-js/pull/83/commits/8efe6e4b6fc031275e5485259e61d4f5b1fe3f2c)

**Cyfrin:** Verified. `Ownable2StepUpgradeable` is now used.
