---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-04-cyfrin-symbiotic-v2-0-2-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-09-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-04-cyfrin-symbiotic-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-04-cyfrin-symbiotic-v2-0
title: '`__NoncesUpgradeable_init` is not invoked'
vuln_class: []
---

# `__NoncesUpgradeable_init` is not invoked

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-04-cyfrin-symbiotic-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-04-cyfrin-symbiotic-v2.0.md)_

---

**Description:** The `__NoncesUpgradeable_init` function from the `NoncesUpgradeable` contract is not being called during the initialization of the `VotingPowerProvider` abstract contract. Since `VotingPowerProvider` inherits from `NoncesUpgradeable`, failing to initialize the nonce-related state can lead to incorrect nonce management, potentially causing issues with replay protection in signature verification or other related functionalities.

**Recommended Mitigation:** Update the `__VotingPowerProvider_init` function to include a call to `__NoncesUpgradeable_init()`

```solidity
function __VotingPowerProvider_init(
VotingPowerProviderInitParams memory votingPowerProviderInitParams
) internal virtual onlyInitializing {
__NetworkManager_init(votingPowerProviderInitParams.networkManagerInitParams);
VotingPowerProviderLogic.initialize(votingPowerProviderInitParams);
__OzEIP712_init(votingPowerProviderInitParams.ozEip712InitParams);
__NoncesUpgradeable_init(); // /@audit Add this line to properly initialize nonce state
}
```

**Symbiotic:** Acknowledged. Not invoked to optimize bytecode size. Should be safe since it's not initializing any state inside

**Cyfrin:** Acknowledged.
