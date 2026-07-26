---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-cryptoart-v2-0-2-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-04-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-cryptoart-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-24-cyfrin-cryptoart-v2-0
title: Signatures have no expiration deadline
vuln_class: []
---

# Signatures have no expiration deadline

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-cryptoart-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-cryptoart-v2.0.md)_

---

**Description:** Signatures which have [no expiration parameter](https://dacian.me/signature-replay-attacks#heading-no-expiration) effectively grant a lifetime license. Consider adding an expiration parameter to the signature that if used after that time results in the signature being invalid.

**CryptoArt:**
Fixed in commit [a93977d](https://github.com/cryptoartcom/cryptoart-smart-contracts/commit/a93977d2ef0b54319c7668d9fc6abda688b355c1).

**Cyfrin:** Verified.
