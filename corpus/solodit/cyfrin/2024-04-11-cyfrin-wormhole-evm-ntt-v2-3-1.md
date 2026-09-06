---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-11-cyfrin-wormhole-evm-ntt-v2-3-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-04-11T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-11-cyfrin-wormhole-evm-ntt-v2.md
tags:
- firm:cyfrin
- report:2024-04-11-cyfrin-wormhole-evm-ntt-v2
title: Incorrect topics[0] documented in `INTTManagerEvents` and `IRateLimiterEvents`
vuln_class: []
---

# Incorrect topics[0] documented in `INTTManagerEvents` and `IRateLimiterEvents`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-11-cyfrin-wormhole-evm-ntt-v2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-11-cyfrin-wormhole-evm-ntt-v2.md)_

---

**Description:** Inline NatSpec documentation incorrectly specifies topics[0] for the following events:

1. [`INTTManagerEvents::TransceiverAdded`](https://github.com/wormhole-foundation/example-native-token-transfers/blob/f4e2277b358349dbfb8a654d19a925628d48a8af/evm/src/interfaces/INttManagerEvents.sol#L51-L52) –
Documented: `0xc6289e62021fd0421276d06677862d6b328d9764cdd4490ca5ac78b173f25883`;
Correct: `0xf05962b5774c658e85ed80c91a75af9d66d2af2253dda480f90bce78aff5eda5`.
2. [`INTTManagerEvents::TransceiverRemoved`](https://github.com/wormhole-foundation/example-native-token-transfers/blob/f4e2277b358349dbfb8a654d19a925628d48a8af/evm/src/interfaces/INttManagerEvents.sol#L59-L60) –
Documented: `0x638e631f34d9501a3ff0295873b29f50d0207b5400bf0e48b9b34719e6b1a39e`;
Correct: `0x697a3853515b88013ad432f29f53d406debc9509ed6d9313dcfe115250fcd18f`.
3. [`IRateLimiterEvents::OutboundTransferRateLimited`](https://github.com/wormhole-foundation/example-native-token-transfers/blob/f4e2277b358349dbfb8a654d19a925628d48a8af/evm/src/interfaces/IRateLimiterEvents.sol#L20-L21) –
Documented: `0x754d657d1363ee47d967b415652b739bfe96d5729ccf2f26625dcdbc147db68b`;
Correct: `0xf33512b84e24a49905c26c6991942fc5a9652411769fc1e448f967cdb049f08a`.

**Wormhole Foundation:** Inline NatSpec docs can be error-prone. Thinking about using Foundry as the source of truth for selectors/topics.

**Cyfrin:** Acknowledged.
