---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-09-cyfrin-wormhole-evm-cctp-v2-1-2-6
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-04-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-09-cyfrin-wormhole-evm-cctp-v2-1.md
tags:
- firm:cyfrin
- report:2024-04-09-cyfrin-wormhole-evm-cctp-v2-1
title: Temporary denial-of-service when in-flight messages are not executed before
  a deprecated Wormhole Guardian set expires
vuln_class: []
---

# Temporary denial-of-service when in-flight messages are not executed before a deprecated Wormhole Guardian set expires

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-09-cyfrin-wormhole-evm-cctp-v2-1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-09-cyfrin-wormhole-evm-cctp-v2-1.md)_

---

**Description:** Wormhole exposes a governance action in [`Governance::submitNewGuardianSet`](https://github.com/wormhole-foundation/wormhole/blob/eee4641f55954d2d0db47831688a2e97eb20f7ee/ethereum/contracts/Governance.sol#L76-L112) to update the Guardian set via Governance VAA.

```solidity
function submitNewGuardianSet(bytes memory _vm) public {
    ...

    // Trigger a time-based expiry of current guardianSet
    expireGuardianSet(getCurrentGuardianSetIndex());

    // Add the new guardianSet to guardianSets
    storeGuardianSet(upgrade.newGuardianSet, upgrade.newGuardianSetIndex);

    // Makes the new guardianSet effective
    updateGuardianSetIndex(upgrade.newGuardianSetIndex);
}
```

When this function is called, [`Setters:: expireGuardianSet`](https://github.com/wormhole-foundation/wormhole/blob/main/ethereum/contracts/Setters.sol#L13-L15) initiates a 24-hour timeframe after which the current guardian set expires.

```solidity
function expireGuardianSet(uint32 index) internal {
    _state.guardianSets[index].expirationTime = uint32(block.timestamp) + 86400;
}
```

Hence, any in-flight VAAs that utilize the deprecated Guardian set index will fail to be executed given the validation present in [`Messages::verifyVMInternal`](https://github.com/wormhole-foundation/wormhole/blob/main/ethereum/contracts/Messages.sol).

```solidity
/// @dev Checks if VM guardian set index matches the current index (unless the current set is expired).
if(vm.guardianSetIndex != getCurrentGuardianSetIndex() && guardianSet.expirationTime < block.timestamp){
    return (false, "guardian set has expired");
}
```

Considering there is no automatic relaying of Wormhole CCTP messages, counter to what is specified in the [documentation](https://docs.wormhole.com/wormhole/quick-start/tutorials/cctp) (unless an integrator implements their own relayer), there are no guarantees that an in-flight message which utilizes an old Guardian set index will be executed by the `mintRecipient` on the target domain within its 24-hour expiration period. This could occur, for example, in cases such as:
1. Integrator messages are blocked by their use of the Wormhole nonce/sequence number.
2. CCTP contracts are paused on the target domain, causing all redemptions to revert.
3. L2 sequencer downtime, since the Wormhole CCTP integration contracts do not consider aliased addresses for forced inclusion.
4. The `mintRecipient` is a contract that has been paused following an exploit, temporarily restricting all incoming and outgoing transfers.

In the current design, it is not possible to update the `mintRecipient` for a given deposit due to the multicast nature of VAAs. CCTP exposes [`MessageTransmitter::replaceMessage`](https://github.com/circlefin/evm-cctp-contracts/blob/1662356f9e60bb3f18cb6d09f95f628f0cc3637f/src/MessageTransmitter.sol#L129-L181) which allows the original source caller to update the destination caller for a given message and its corresponding attestation; however, the Wormhole CCTP integration currently provides no access to this function and has no similar functionality of its own to allow updates to the target `mintRecipient` of the VAA.

Additionally, there is no method for forcibly executing the redemption of USDC/EURC to the `mintRecipient`, which is the only address allowed to execute the VAA on the target domain, as validated in [`Logic::redeemTokensWithPayload`](https://github.com/wormhole-foundation/wormhole-circle-integration/blob/f7df33b159a71b163b8b5c7e7381c0d8f193da99/evm/src/contracts/CircleIntegration/Logic.sol#L61-L108).

```solidity
// Confirm that the caller is the `mintRecipient` to ensure atomic execution.
require(
    msg.sender.toUniversalAddress() == deposit.mintRecipient, "caller must be mintRecipient"
);
```

Without any programmatic method for replacing expired VAAs with new VAAs signed by the updated Guardian set, the source USDC/EURC will be burnt, but it will not be possible for the expired VAAs to be executed, leading to denial-of-service on the `mintRecipient` receiving tokens on the target domain. The Wormhole CCTP integration does, however, inherit some mitigations already in place for this type of scenario where the Guardian set is updated, as explained in the [Wormhole whitepaper](https://github.com/wormhole-foundation/wormhole/blob/eee4641f55954d2d0db47831688a2e97eb20f7ee/whitepapers/0003_token_bridge.md#caveats), meaning that it is possible to repair or otherwise replace the expired VAA for execution using signatures from the new Guardian set. In all cases, the original VAA metadata remains intact since the new VAA Guardian signatures refer to an event that has already been emitted, so none of the contents of the VAA payload besides the Guardian set index and associated signatures change on re-observation. This means that the new VAA can be safely paired with the existing Circle attestation for execution on the target domain by the original `mintRecipient`.

**Impact:** There is only a single address that is permitted to execute a given VAA on the target domain; however, there are several scenarios that have been identified where this `mintReceipient` may be unable to perform redemption for a period in excess of 24 hours following an update to the Guardian set while the VAA is in-flight. Fortunately, Wormhole Governance has a well-defined path to resolution, so the impact is limited.

**Proof of Concept:**
1. Alice burns 100 USDC to be transferred to dApp X from CCTP Domain A to CCTP Domain B.
2. Wormhole executes a Governance VAA to update the Guardian set.
3. 24 hours pass, causing the previous Guardian set to expire.
4. dApp X attempts to redeem 100 USDC on CCTP Domain B, but VAA verification fails because the message was signed using the expired Guardian set.
5. The 100 USDC remains burnt and cannot be minted on the target domain by executing the attested CCTP message until the expired VAA is reobserved by members of the new Guardian set.

**Recommended Mitigation:** The practicality of executing the proposed Governance mitigations at scale should be carefully considered, given the extent to which USDC is entrenched within the wider DeFi ecosystem. There is a high likelihood of temporary widespread, high-impact DoS, although this is somewhat limited by the understanding that Guardian set updates are expected to occur relatively infrequently, given there have only been three updates in the lifetime of Wormhole so far. There is also potentially insufficient tooling for the detailed VAA re-observation scenarios, which should handle the recombination of the signed CCTP message with the new VAA and clearly communicate these considerations to integrators.

**Wormhole Foundation:** This is the same as how the Wormhole token bridge operates.

**Cyfrin:** Acknowledged.
