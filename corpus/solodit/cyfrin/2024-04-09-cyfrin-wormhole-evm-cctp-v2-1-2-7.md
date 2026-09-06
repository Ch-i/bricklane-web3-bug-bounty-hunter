---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-09-cyfrin-wormhole-evm-cctp-v2-1-2-7
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
title: The `mintRecipient` address should be required to indicate interface support
  to prevent potential loss of funds
vuln_class: []
---

# The `mintRecipient` address should be required to indicate interface support to prevent potential loss of funds

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-09-cyfrin-wormhole-evm-cctp-v2-1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-09-cyfrin-wormhole-evm-cctp-v2-1.md)_

---

If the destination `mintRecipient` is a smart contract, it should be required to implement `IERC165` and another Wormhole/CCTP-specific interface to ensure that it has the necessary functionality to transfer/approve USDC/EURC tokens. Whilst it is ultimately the responsibility of the integrator to ensure that they correctly handle the receipt of tokens, this recommendation should help to avoid situations where the tokens become irreversibly stuck after calling `Logic::redeemTokenWithPayload`.

**Wormhole Foundation:** Responsibility lies with the integrator to ensure their code works with the `CircleIntegration` logic.

**Cyfrin:** Acknowledged.

\clearpage
