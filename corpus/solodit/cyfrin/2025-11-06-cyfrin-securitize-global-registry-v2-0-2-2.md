---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-06-cyfrin-securitize-global-registry-v2-0-2-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-11-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-06-cyfrin-securitize-global-registry-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-06-cyfrin-securitize-global-registry-v2-0
title: '`GlobalRegistryService::executePreApprovedTransaction` is incompatible with
  smart wallet operators'
vuln_class: []
---

# `GlobalRegistryService::executePreApprovedTransaction` is incompatible with smart wallet operators

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-06-cyfrin-securitize-global-registry-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-06-cyfrin-securitize-global-registry-v2.0.md)_

---

**Description:** `GlobalRegistryService::executePreApprovedTransaction` allows an operator to execute pre-approved transactions using signatures. However it always calls `ECDSA::recover` which means it won't work for operators who are smart wallets.

This appears to be the intention but if smart wallet support is desired consider using the [SignatureChecker](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/cryptography/SignatureChecker.sol) library.

**Securitize:** Acknowledged; we know the signer (who is always an "Operator") does not use smart wallets.
