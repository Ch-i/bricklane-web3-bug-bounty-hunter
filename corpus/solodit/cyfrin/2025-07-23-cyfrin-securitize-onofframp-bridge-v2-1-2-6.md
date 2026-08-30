---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1-2-6
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-07-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1
title: '`whChainId` should not be stored as immutable constant'
vuln_class: []
---

# `whChainId` should not be stored as immutable constant

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md)_

---

**Description:** The `SecuritizeBridge` contract's use of an immutable `whChainId` constant, set during deployment, creates a critical vulnerability during chain forks. If the stored whChainId no longer matches the actual `chain ID`(block.chainid), cross-chain operations via `sendPayloadToEvm` may use an incorrect source chain ID.

**Impact:** This mismatch can cause cross-chain message deliveries to fail or refunds to process incorrectly, disrupting the contract's functionality. As a result, funds may become locked in the refund flow, leading to financial loss for users and undermining trust in the system’s reliability.

**Recommended Mitigation:** Replace the immutable `whChainId` with dynamic chain ID retrieval:

```solidity
// Remove: uint16 public immutable whChainId;

function getCurrentChainId() public view returns (uint16) {
    return uint16(block.chainid);
}

// In bridgeDSTokens function:
wormholeRelayer.sendPayloadToEvm{value: msg.value} (
    targetChain,
    targetAddress,
    abi.encode(/* payload data */),
    0,
    gasLimit,
    getCurrentChainId(),
    msg.sender
);
```

**Securitize:** Rejected. `whChainId` is not the EVM chain id, it's the Wormhole-specific chain id that is defined [here](https://wormhole.com/docs/build/reference/chain-ids/).

**Cyfrin:** Acknowledged.
