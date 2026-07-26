---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-11-cyfrin-wormhole-evm-ntt-v2-2-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-04-11T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-11-cyfrin-wormhole-evm-ntt-v2.md
tags:
- firm:cyfrin
- report:2024-04-11-cyfrin-wormhole-evm-ntt-v2
title: Inconsistent implementation of ERC-7201 Namespaced Storage locations
vuln_class: []
---

# Inconsistent implementation of ERC-7201 Namespaced Storage locations

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-11-cyfrin-wormhole-evm-ntt-v2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-11-cyfrin-wormhole-evm-ntt-v2.md)_

---

**Description:** Regarding the implementation of Namespaced Storage locations, the EIP-7201 formula should be followed to strictly conform to the EIP specification, as is correctly done by the modified OpenZeppelin libraries in `libraries/external`; elsewhere, usage is incorrect.

Additionally, there are instances where the location strings appear inconsistent, for example, `Pause.pauseRole`, which should likely instead be `Pauser.pauserRole`.

**Impact:** Namespaces are implemented to avoid collisions with other namespaces or the standard Solidity storage layout. The formula defined in EIP-7201 guarantees this property for arbitrary namespace IDs under the assumption of keccak256 collision resistance. It is, therefore, important to ensure that its implementation is consistent to fully benefit from these assurances.

**Recommended Mitigation:** Use the formula outlined in the [EIP](https://eips.ethereum.org/EIPS/eip-7201) to update all other instances in `src/*`:
```solidity
keccak256(abi.encode(uint256(keccak256("example.location")) - 1)) & ~bytes32(uint256(0xff));
```

**Wormhole Foundation:** Although we don’t conform to the EIP, we believe our storage slots are still collision-resistant.

**Cyfrin:** Acknowledged.
