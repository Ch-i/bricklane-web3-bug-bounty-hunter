---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-2-10
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-07-07T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-07-cyfrin-suzaku-core-v2-0
title: '`remainingBalanceOwner` should be set by the protocol owner'
vuln_class: []
---

# `remainingBalanceOwner` should be set by the protocol owner

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-07-cyfrin-suzaku-core-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md)_

---

**Description:** The `remainingBalanceOwner` parameter, passed during the invocation of the `addNode` function, is intended to represent the P-Chain owner address that will receive any leftover `$AVAX` from a validator's balance when the validator is removed from the validator set. Currently, this value is provided by the operator invoking `addNode`.

However, from a protocol security and correctness perspective, the assignment of `remainingBalanceOwner` should not be left to the operator. Instead, this should be determined and configured by the protocol itself to prevent wrong party receiving leftover funds.

Example snippet from the function signature:

```solidity
function addNode(
        bytes32 nodeId,
        bytes calldata blsKey,
        uint64 registrationExpiry,
        PChainOwner calldata remainingBalanceOwner, // should be passed by the protocol
        PChainOwner calldata disableOwner,
        uint256 stakeAmount // optional
    ) external updateStakeCache(getCurrentEpoch(), PRIMARY_ASSET_CLASS) updateGlobalNodeStakeOncePerEpoch {
```

**Impact:** Misrouting of leftover \$AVAX funds upon validator removal, potentially enabling loss of funds for the stakers.

**Recommended Mitigation:** Modify the protocol to internally assign the `remainingBalanceOwner` during the `addNode` operation, removing this parameter from operator input.

```diff
function addNode(
        bytes32 nodeId,
        bytes calldata blsKey,
        uint64 registrationExpiry,
-        PChainOwner calldata remainingBalanceOwner,
        PChainOwner calldata disableOwner,
        uint256 stakeAmount // optional
    ) external updateStakeCache(getCurrentEpoch(), PRIMARY_ASSET_CLASS) updateGlobalNodeStakeOncePerEpoch {

}

```

**Suzaku:**
Acknowledged.

**Cyfrin:** Acknowledged.
