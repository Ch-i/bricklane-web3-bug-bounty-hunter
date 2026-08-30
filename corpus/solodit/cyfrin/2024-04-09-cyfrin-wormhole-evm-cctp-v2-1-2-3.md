---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-09-cyfrin-wormhole-evm-cctp-v2-1-2-3
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-04-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-09-cyfrin-wormhole-evm-cctp-v2-1.md
tags:
- firm:cyfrin
- report:2024-04-09-cyfrin-wormhole-evm-cctp-v2-1
title: Potential dangers for inheriting applications executing the Wormhole payload
vuln_class: []
---

# Potential dangers for inheriting applications executing the Wormhole payload

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-09-cyfrin-wormhole-evm-cctp-v2-1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-09-cyfrin-wormhole-evm-cctp-v2-1.md)_

---

The Wormhole CCTP contracts are written to allow integration by both composition and inheritance. When calling `Logic::transferTokensWithPayload`, users are able to pass an arbitrary [Wormhole payload](https://github.com/wormhole-foundation/wormhole-circle-integration/blob/bbc593d7f4caf2b59bf9de18a870e2df37ed6fd4/evm/src/contracts/CircleIntegration/Logic.sol#L34) that gets [parsed from the VAA](https://github.com/wormhole-foundation/wormhole-circle-integration/blob/bbc593d7f4caf2b59bf9de18a870e2df37ed6fd4/evm/src/contracts/CircleIntegration/Logic.sol#L83) on the destination chain. It is our understanding that, if required, execution of this payload is intended to be the responsibility of the integrating application. As such, it has been noted that the behavior of payload execution has not been tested; however, the Wormhole payload does not necessarily need to be executed with an external call, since it could simply contain information that is useful to the inheriting contract.

In the case the payload is used as the input for an arbitrary external call, there is a risk here for the integrator. For applications inheriting the Wormhole CCTP contracts, execution of the payload will occur in the context of these contracts, which could be potentially dangerous. It is, therefore, the responsibility of the integrator to perform sufficient application-specific validation on the payload. This should be clearly documented.

**Wormhole Foundation:** The existing functionality is as intended.

**Cyfrin:** Acknowledged.
