---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-09-cyfrin-wormhole-evm-cctp-v2-1-2-5
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-04-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-09-cyfrin-wormhole-evm-cctp-v2-1.md
tags:
- firm:cyfrin
- report:2024-04-09-cyfrin-wormhole-evm-cctp-v2-1
title: Calldata restriction on Wormhole payload should not be modified
vuln_class: []
---

# Calldata restriction on Wormhole payload should not be modified

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-09-cyfrin-wormhole-evm-cctp-v2-1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-09-cyfrin-wormhole-evm-cctp-v2-1.md)_

---

Based on an end-to-end fork test written between Arbitrum and Avalanche C-Chain (15M block gas limit), a gas usage of ~2.5M units has been observed using the maximum allowed payload length of `type(uint16).max`. It is important that this calldata restriction is not modified; otherwise, a scenario could exist where it may not be possible for the `mintRecipient` to execute redemptions on the target domain due to an out-of-gas error caused by an [excessively large Wormhole payload](https://solodit.xyz/issues/h-2-malicious-user-can-use-an-excessively-large-_toaddress-in-oftcoresendfrom-to-break-layerzero-communication-sherlock-uxd-uxd-protocol-git). Even in the current state, integrators should be careful to ensure that any additional calls wrapping those to `Logic::redeemTokensWithPayload` cannot be made susceptible to this issue.

**Wormhole Foundation:** Acknowledged.

**Cyfrin:** Acknowledged.
