---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-3-20
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: Protocol classifies retail investors based solely on whether they are qualified
  investors, without checking if they are accredited investors
vuln_class: []
---

# Protocol classifies retail investors based solely on whether they are qualified investors, without checking if they are accredited investors

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** The protocol classifies "retail investors" based solely on whether they are qualified investors, without checking if they are accredited investors. Throughout the codebase, retail investors are identified using `!RegistryService::isQualifiedInvestor()`, but for US investors the correct definition would be `!isQualifiedInvestor() && !isAccreditedInvestor()`.

**Impact:** In the current configuration:
* `isRetail` and the other related checks are only ever performed for EU investors
* non-retail EU investors are marked using the `Qualified` attribute

So while the current code appears to be fine as it is only used for EU investors, a bug could easily be introduced in the future if a developer calls `isRetail` in relation to US investors or adopts the pattern in other places but for US investors.

**Recommended Mitigation:** Considering either renaming `isRetail` or adding an explanatory comment directly above it to indicate that this function should only be used for EU investors.

**Securitize:** This is the correct behavior as this function should only be used for EU investors; in commit [6aef381](https://github.com/securitize-io/dstoken/commit/6aef381b1c88df0a376557f41bd900af8f1a0fe1) we've added comments explaining this.

**Cyfrin:** Verified.
