---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-24-cyfrin-linea-1-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-05-24T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-24-cyfrin-linea.md
tags:
- firm:cyfrin
- report:2024-05-24-cyfrin-linea
title: Users can't cancel or refund their source chain transaction if the destination
  chain transaction continually fails, causing loss of bridged funds
vuln_class: []
---

# Users can't cancel or refund their source chain transaction if the destination chain transaction continually fails, causing loss of bridged funds

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-24-cyfrin-linea.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-24-cyfrin-linea.md)_

---

**Description:** Linea's messaging service allows users to bridge ETH between Ethereum L1 mainnet and Linea L2.

The bridging process operates in 2 distinct transactions where the first can succeed and the second can fail completely independently of each other.

In the first step of the bridging process on the source chain the user supplies their ETH to the messaging service contract on that chain together with some parameters.

In the last step of the bridging process on the destination chain a delivery service ("postman") or the user themselves calls `claimMessage` or `claimMessageWithProof` to complete the bridging process.

The last step of claiming the message is an arbitrary [call](https://github.com/Consensys/zkevm-monorepo/blob/364b64d2a2704567adac00e3fa428a1901717666/contracts/contracts/messageService/l1/L1MessageService.sol#L144-L154) with arbitrary calldata made to an address of the user's choosing. If this call fails for any reason the user may re-try claiming the message an infinite number of times. However if this call continues to revert (or if the `claim` transaction continually reverts for any other reason), the user:
* will never receive their bridged ETH on the destination chain
* has no way of initiating a cancel or refund transaction on the source chain

**Impact:** This scenario will result in a loss of bridged funds to the user.

**Recommended Mitigation:** Implement a cancel or refund mechanism that users can initiate on the source chain to retrieve their funds if the claim transaction continually reverts on the destination chain.

**Linea:**
Acknowledged. Currently there is no cancellation or refund feature but users can re-try the destination chain delivery as many times as they like. We may consider implementing this in the future.

\clearpage
