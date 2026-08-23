---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-3-21
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: Not possible to rehash `DOMAIN_SEPARATOR` in `MultiSigWallet` to update chainId
  if is ever required
vuln_class: []
---

# Not possible to rehash `DOMAIN_SEPARATOR` in `MultiSigWallet` to update chainId if is ever required

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** `MultiSigWallet` does not have a function to rehash the `DOMAIN_SEPARATOR` in case it is required to update the chainId, which was used for the initial DOMAIN_SEPARATOR when the contract was deployed.

**Recommended Mitigation:** Consider adding a function similar to `TransactionRelayer::updatedomainSeparator()` to allow updating the `DOMAIN_SEPARATOR` in the MultiSigWallet

**Securitize:** `MultiSigWallet` was removed as it is deprecated.

**Cyfrin:** Verified.
