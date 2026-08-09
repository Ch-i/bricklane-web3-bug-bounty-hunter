---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-06-cyfrin-securitize-global-registry-v2-0-3-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-11-06T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-06-cyfrin-securitize-global-registry-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-06-cyfrin-securitize-global-registry-v2-0
title: Remove unused `ExecutePreApprovedTransaction::nonce`
vuln_class: []
---

# Remove unused `ExecutePreApprovedTransaction::nonce`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-06-cyfrin-securitize-global-registry-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-06-cyfrin-securitize-global-registry-v2.0.md)_

---

**Description:** `ExecutePreApprovedTransaction::nonce` is never actually used, since:

* `GlobalRegistryService::hashTx` always reads the current nonce from storage `noncePerInvestor[txData.senderInvestor]`
* the caller must have used the current nonce to sign - otherwise the signature will fail validation
* when validation succeeds, `executePreApprovedTransaction` always increments the current nonce by 1 so it can never be re-used

Hence the above mechanics correctly validate the nonce and `ExecutePreApprovedTransaction::nonce` can be safely removed as it is never used.

**Securitize:** Fixed in commit [c841572](https://github.com/securitize-io/bc-global-registry-service-sc/commit/c841572de8b7dcfee484f6f7f4ce9a19e579bf21).

**Cyfrin:** Verified.

\clearpage
