---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-17-cyfrin-quantamm-v1-2-1-4
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-12-17T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-quantamm-v1.2.md
tags:
- firm:cyfrin
- report:2024-12-17-cyfrin-quantamm-v1-2
title: Missing admin functions prevent execution of key `UpdateWeightRunner` actions
vuln_class: []
---

# Missing admin functions prevent execution of key `UpdateWeightRunner` actions

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-17-cyfrin-quantamm-v1.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-quantamm-v1.2.md)_

---

**Description:** Several functions in `UpdateWeightRunner` require the `quantammAdmin` role, but these functions are missing from `QuantAMMBaseAdministration`. The affected functions are:

* [`UpdateWeightRunner::addOracle`](https://github.com/QuantAMMProtocol/QuantAMM-V1/blob/7213401491f6a8fd1fcc1cf4763b15b5da355f1c/pkg/pool-quantamm/contracts/UpdateWeightRunner.sol#L182-L195)
* [`UpdateWeightRunner::removeOracle`](https://github.com/QuantAMMProtocol/QuantAMM-V1/blob/7213401491f6a8fd1fcc1cf4763b15b5da355f1c/pkg/pool-quantamm/contracts/UpdateWeightRunner.sol#L197-L203)
* [`UpdateWeightRunner::setApprovedActionsForPool`](https://github.com/QuantAMMProtocol/QuantAMM-V1/blob/7213401491f6a8fd1fcc1cf4763b15b5da355f1c/pkg/pool-quantamm/contracts/UpdateWeightRunner.sol#L205-L209)
* [`UpdateWeightRunner::setETHUSDOracle`](https://github.com/QuantAMMProtocol/QuantAMM-V1/blob/7213401491f6a8fd1fcc1cf4763b15b5da355f1c/pkg/pool-quantamm/contracts/UpdateWeightRunner.sol#L281-L287)

Since these functions rely on `quantammAdmin`, they cannot be executed unless the corresponding calls are included in `QuantAMMBaseAdministration`.

**Impact:** The `QuantAMMBaseAdministration` contract cannot execute the above functions. As a result, administrative actions such as adding or removing oracles, setting approved actions for pools, and updating the ETH/USD oracle cannot be performed, limiting the functionality and flexibility of the system.

**Recommended Mitigation:** Consider one of the following approaches:

1. Add the Missing Functions to `QuantAMMBaseAdministration`
2. Use OpenZeppelin’s `TimeLock` Contract Directly:
   If `QuantAMMBaseAdministration` is redundant, replace it with OpenZeppelin's `TimeLock` contract to manage administrative functions securely and effectively.

**QuantAMM:** Fixed in [`a299ce7`](https://github.com/QuantAMMProtocol/QuantAMM-V1/commit/a299ce72076b58503386bc146b81014560536d9e)

**Cyfrin:** Verified. `QuantAMMBaseAdministration` is removed.
