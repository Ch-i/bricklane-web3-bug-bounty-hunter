---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-08-28-cyfrin-securitize-tempo-tip20-v2-0-2-13
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
title: '`Tip20RegistryService::registerInvestorWithWallets, isAuthorized` mishandle
  Tempo virtual addresses'
vuln_class: []
---

# `Tip20RegistryService::registerInvestorWithWallets, isAuthorized` mishandle Tempo virtual addresses

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md)_

---

**Description:** Tempo TIP-20 resolves a virtual recipient address to its registered master before recipient validation and transfer-policy authorization, while TIP-403 rejects virtual aliases as policy members and requires configuration of the resolved master. `Tip20RegistryService::registerInvestorWithWallets` forwards the supplied wallet unchanged to `ITIP403::modifyPolicyWhitelist`, so onboarding a virtual alias reverts. Conversely, after the master is registered and whitelisted, a TIP-20 transfer to its virtual alias can succeed after resolution while `Tip20RegistryService::isAuthorized` forwards the raw alias to `ITIP403::isAuthorized` and returns false ([TIP-20 specification](https://tempo.xyz/developers/docs/protocol/tip20/spec), [TIP-403 specification](https://tempo.xyz/developers/docs/protocol/tip403/spec)).

**Impact:** Integrations that accept Tempo virtual addresses either fail holder onboarding or report an authorization result that differs from the native token's effective recipient authorization.

**Recommended Mitigation:** Document on `registerInvestorWithWallets` and `isAuthorized` that callers must supply resolved master addresses rather than virtual aliases.

**Securitize:** Fixed in [PR 19](https://github.com/securitize-io/bc-tempo-sc/pull/19).

**Cyfrin:** Verified.
