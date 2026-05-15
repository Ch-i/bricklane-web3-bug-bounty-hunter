---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-11-cyfrin-wormhole-evm-ntt-v2-4-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-04-11T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-11-cyfrin-wormhole-evm-ntt-v2.md
tags:
- firm:cyfrin
- report:2024-04-11-cyfrin-wormhole-evm-ntt-v2
title: Unnecessary type casts of proxied storage slots from `bytes32` to `uint256`
vuln_class: []
---

# Unnecessary type casts of proxied storage slots from `bytes32` to `uint256`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-11-cyfrin-wormhole-evm-ntt-v2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-11-cyfrin-wormhole-evm-ntt-v2.md)_

---

There are multiple instances where proxied storage slots are cast from type `bytes32` to `uint256`; however, this is not necessary as the EVM uses 32-byte words, meaning that these types are interchangeable when considering the subsequent inline assembly assignment. One example can be found in [`Governance::_getConsumedGovernanceActionsStorage`](https://github.com/wormhole-foundation/example-native-token-transfers/blob/f4e2277b358349dbfb8a654d19a925628d48a8af/evm/src/wormhole/Governance.sol#L34-L43):

```solidity
function _getConsumedGovernanceActionsStorage()
    private
    pure
    returns (mapping(bytes32 => bool) storage $)
{
    uint256 slot = uint256(CONSUMED_GOVERNANCE_ACTIONS_SLOT);
    assembly ("memory-safe") {
        $.slot := slot
    }
}
```

Consider [removing this type cast](https://github.com/OpenZeppelin/openzeppelin-contracts-upgradeable/blob/789ba4f167cc94088e305d78e4ae6f3c1ec2e6f1/contracts/utils/PausableUpgradeable.sol#L25-L31) to save gas.

**Wormhole Foundation:** To do this we could have to precompute the constants since this otherwise leads to a compiler error.

**Cyfrin:** Acknowledged.
