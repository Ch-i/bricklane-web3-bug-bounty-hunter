---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-cryptoart-v2-0-2-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-04-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-cryptoart-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-24-cyfrin-cryptoart-v2-0
title: Protocol vulnerable to cross-chain signature replay
vuln_class: []
---

# Protocol vulnerable to cross-chain signature replay

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-cryptoart-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-cryptoart-v2.0.md)_

---

**Description:** As signatures do not include`chainId`, signature verification is vulnerable to [cross-chain replay](https://dacian.me/signature-replay-attacks#heading-cross-chain-replay).

**Impact:** Although the protocol plans to deploy cross-chain in the future, the specification of this audit is to only consider deployment to one chain. Hence this finding is only Informational as this attack path is not possible when the protocol is only deployed on one chain.

**Recommended Mitigation:** Include `block.chainid` as a signature parameter.

**CryptoArt:**
Fixed in commit [1e25f8c](https://github.com/cryptoartcom/cryptoart-smart-contracts/commit/1e25f8cd172a32e3e35ccf8a86e7af9fe1ed47fe).

**Cyfrin:** Verified.
