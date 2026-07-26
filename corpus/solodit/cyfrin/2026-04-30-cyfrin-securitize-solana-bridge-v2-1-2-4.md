---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-30-cyfrin-securitize-solana-bridge-v2-1-2-4
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-04-30T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-30-cyfrin-securitize-solana-bridge-v2-1
title: Pause blocks inbound VAA execution, stranding in-flight cross-chain transfers
vuln_class: []
---

# Pause blocks inbound VAA execution, stranding in-flight cross-chain transfers

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md)_

---

**Description:** When paused, both `BridgeDsTokens::handler` (outbound) and `ExecuteVaaV1::handler` (inbound) are disabled by `constraint = !config.paused`. This blocks processing of valid Wormhole VAAs representing tokens already burned on the source chain. There is a single pause flag controlling both directions.

**Impact:** In-flight transfers are temporarily stranded during pause. Tokens are not permanently lost -- admin can unpause to process pending VAAs. Permanent stranding only if combined with owner key loss while paused.

**Recommended Mitigation:** Implement separate pause flags for outbound and inbound operations, allowing inbound VAA processing during outbound pause.

**Securitize:** Acknowledged. The unified pause flag is an intentional design choice: during an incident, halting both directions is the desired safety posture. In-flight VAAs are not time-bound and can be executed after unpause without loss of funds, so we accept this trade-off and will not introduce separate pause flags.
