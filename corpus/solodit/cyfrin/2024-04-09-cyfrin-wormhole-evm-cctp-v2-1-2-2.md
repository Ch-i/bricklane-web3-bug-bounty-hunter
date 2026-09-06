---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-09-cyfrin-wormhole-evm-cctp-v2-1-2-2
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-04-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-09-cyfrin-wormhole-evm-cctp-v2-1.md
tags:
- firm:cyfrin
- report:2024-04-09-cyfrin-wormhole-evm-cctp-v2-1
title: '`Setup` unnecessarily inherits OpenZeppelin `Context`'
vuln_class: []
---

# `Setup` unnecessarily inherits OpenZeppelin `Context`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-09-cyfrin-wormhole-evm-cctp-v2-1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-09-cyfrin-wormhole-evm-cctp-v2-1.md)_

---

The `Setup` contract currently inherits OpenZeppelin `Context`; however, this is unnecessary as none of its functionality is used anywhere within the logic.

**Wormhole Foundation:** Fixed in [PR \#52](https://github.com/wormhole-foundation/wormhole-circle-integration/pull/52).

**Cyfrin:** Acknowledged.
