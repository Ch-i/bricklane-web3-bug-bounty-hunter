---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-08-28-cyfrin-securitize-tempo-tip20-v2-0-2-11
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-08-28T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md
tags:
- firm:cyfrin
- report:2026-08-28-cyfrin-securitize-tempo-tip20-v2-0
title: '`Tip20RegistryService::addPlatformWallet` has an unreachable duplicate check'
vuln_class: []
---

# `Tip20RegistryService::addPlatformWallet` has an unreachable duplicate check

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md)_

---

**Description:** `Tip20RegistryService::addPlatformWallet` calls `_assertRegisterableWallet`, which already rejects an existing platform wallet. The following duplicate check tests the same condition and can never execute.

**Recommended Mitigation:** Remove the second check.

**Securitize:** Fixed in [PR 19](https://github.com/securitize-io/bc-tempo-sc/pull/19).

**Cyfrin:** Verified.
