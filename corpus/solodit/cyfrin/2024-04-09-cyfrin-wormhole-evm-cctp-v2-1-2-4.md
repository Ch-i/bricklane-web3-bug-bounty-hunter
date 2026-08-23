---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-09-cyfrin-wormhole-evm-cctp-v2-1-2-4
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-04-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-09-cyfrin-wormhole-evm-cctp-v2-1.md
tags:
- firm:cyfrin
- report:2024-04-09-cyfrin-wormhole-evm-cctp-v2-1
title: Sequencing considerations should be clearly documented and communicated to
  integrators
vuln_class: []
---

# Sequencing considerations should be clearly documented and communicated to integrators

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-09-cyfrin-wormhole-evm-cctp-v2-1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-09-cyfrin-wormhole-evm-cctp-v2-1.md)_

---

The Wormhole CCTP integration contracts do not enforce in-sequence message execution by default as a design choice to prevent one message from blocking subsequent messages, instead opting to give integrators the ability to order transactions if they so need. Given it is the responsibility of integrating protocols to execute or otherwise consume the Wormhole payload transmitted by the integration contracts, it is possible for out-of-order executions to cause issues with both high severity and high likelihood if the ordering of message execution is not correctly handled. Wormhole VAAs do not have to be ordered and are effectively multicast, so this does not affect the integration insofar as the contracts in scope for this audit are concerned.

When it comes to handling generic payloads along with token transfers across different chains, corruption of the intended order could have non-trivial consequences for operations that are sensitive to order or timing, such as in lending or derivatives, given how deeply USDC is entrenched within the whole of DeFi. Consider the following scenario:
1. Alice transfers 1000 USDC from CCTP Domain A to Perp X on CCTP Domain B.
2. Alice sends another 100 USDC to Perp X, with a payload to open a 5000 USDC position at 5X leverage.
3. Alice's messages are executed on CCTP Doman B:
    1. If the first message is executed before the second, Alice has a margin of 1100, and the trade is correctly created on X.
    2. If the second message is executed before the first, the trade cannot be opened due to insufficient margin. Factoring in liquidations, auctions, and so on, out-of-sequence execution can have a plethora of unintended consequences.

As noted above, the sender has the ability to specify a Wormhole nonce, and there is also a Wormhole sequence number that is auto-incremented. These are both received on the destination chain in the VAA, so integrators wishing to enforce order can do so either by auto-incrementing the Wormhole nonce on the source domain or by using the Wormhole sequence number and then enforcing ordering on the target domain by checking the source chain, sender address, and nonce/sequence. This should be clearly documented and communicated to users.

**Wormhole Foundation:** Integrators requiring ordered transactions will have to enforce this themselves, which is intended behavior.

**Cyfrin:** Acknowledged.
