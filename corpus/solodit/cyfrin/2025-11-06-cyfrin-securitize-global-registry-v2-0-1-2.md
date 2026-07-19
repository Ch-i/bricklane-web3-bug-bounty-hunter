---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-06-cyfrin-securitize-global-registry-v2-0-1-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-11-06T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-06-cyfrin-securitize-global-registry-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-06-cyfrin-securitize-global-registry-v2-0
title: Missing signature deadline for `GlobalRegistryService::executePreApprovedTransaction`
vuln_class: []
---

# Missing signature deadline for `GlobalRegistryService::executePreApprovedTransaction`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-06-cyfrin-securitize-global-registry-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-06-cyfrin-securitize-global-registry-v2.0.md)_

---

**Description:** `GlobalRegistryService::executePreApprovedTransaction` allows an `Operator` to call an arbitrary contract and function, though the current intent is for it to call `addGlobalInvestorWallet`.

**Impact:** While `addGlobalInvestorWallet` implements a deadline using `block.number` (see other issue about using timestamp), if `executePreApprovedTransaction` is used to call other functions then no deadline check may be implemented or deadline checks will need to be duplicated in many other places.

**Recommended Mitigation:** Implement a timestamp-based deadline check in `GlobalRegistryService::executePreApprovedTransaction`. Also consider adding a way for admin or operators to increase `noncePerInvestor[txData.senderInvestor]` so that nonces can be invalidated.

**Securitize:** Fixed in commits [8f92757](https://github.com/securitize-io/bc-global-registry-service-sc/commit/8f927571c7526817ffe43c5f37d11560e79809d9), [e99c56f](https://github.com/securitize-io/bc-global-registry-service-sc/commit/e99c56fe94f9b41e0680d2318f504fca33be4919), [920e496](https://github.com/securitize-io/bc-global-registry-service-sc/commit/920e4965bb9306203a8251e58c962f4dfff67a3f)

**Cyfrin:** Verified.

\clearpage
