---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-cryptoart-v2-0-2-4
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-04-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-cryptoart-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-24-cyfrin-cryptoart-v2-0
title: Remove unused constant `CryptoartNFT::ROYALTY_BASE`
vuln_class: []
---

# Remove unused constant `CryptoartNFT::ROYALTY_BASE`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-cryptoart-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-cryptoart-v2.0.md)_

---

**Description:** The `CryptoartNFT` contract defines a constant `ROYALTY_BASE` with a value of 10,000 that is never used in the contract. This constant is intended to represent the denominator for royalty percentage calculations (where 10,000 = 100%), but it's not referenced anywhere in the contract's implementation.

**Recommended Mitigation:** Remove the unused constant to improve code clarity and reduce deployment gas costs.

**Cryptoart:**
Fixed in commit [0c0dd8c](https://github.com/cryptoartcom/cryptoart-smart-contracts/commit/0c0dd8c8d01e1b5b396852d38faceee007b37891).

**Cyfrin:** Verified.

\clearpage
