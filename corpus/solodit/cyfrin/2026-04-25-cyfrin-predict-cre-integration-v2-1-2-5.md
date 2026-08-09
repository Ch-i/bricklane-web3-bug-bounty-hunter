---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-25-cyfrin-predict-cre-integration-v2-1-2-5
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-04-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-25-cyfrin-predict-cre-integration-v2-1
title: Deployer EOA retains `DEFAULT_ADMIN_ROLE` after deployment
vuln_class: []
---

# Deployer EOA retains `DEFAULT_ADMIN_ROLE` after deployment

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-25-cyfrin-predict-cre-integration-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md)_

---

**Description:** `ChainlinkReceiverBase`'s constructor grants `DEFAULT_ADMIN_ROLE` to `msg.sender` (the deployer EOA, loaded from the `BSC_MAINNET_KEY` / `BSC_TESTNET_KEY` env var). `ChainlinkUpDownAdapterDeployment.s.sol` then grants the same role to the configured multisig but does NOT revoke the deployer's role. After deployment, two principals hold `DEFAULT_ADMIN_ROLE`: the multisig (intended) and the deployer EOA (unintended).

The protocol's documented trust model places administrative authority with the multisig. A second admin principal that isn't the multisig expands the actual trust surface beyond the documented model — the adapter can be fully administered by whoever controls the deployer key, independent of the multisig's state.

**Impact:** Any action `DEFAULT_ADMIN_ROLE` can perform (granting `PAUSER_ROLE` / `EMERGENCY_CLOSE_ROUND_ROLE` to new addresses, rotating the forwarder address, changing the expected author/workflow name, enabling/disabling round configs) is available to the deployer key as well as the multisig. The practical centralization footprint depends on how the deployer key is managed post-deploy. If the deployer is a hot CI key or a developer workstation, the protocol's effective trust model is weaker than the multisig-only model documented.

**Recommended Mitigation:** In `ChainlinkUpDownAdapterDeployment.s.sol`, after granting `DEFAULT_ADMIN_ROLE` to the multisig and the other roles to their holders, revoke the deployer's role in the same transaction:

```solidity
// After all grantRole calls at the end of run():
chainlinkUpDownAdapter.renounceRole(
    chainlinkUpDownAdapter.DEFAULT_ADMIN_ROLE(),
    vm.addr(deployerPrivateKey)
);
```

Verify post-deploy via `hasRole(DEFAULT_ADMIN_ROLE, deployer)` that the deployer no longer holds admin and the multisig is the sole admin principal.

**Predict.fun:** Acknowledged; typically we use the multisig to revoke the role of the deployer key so that we can be sure the multisig has the default admin role. Otherwise, we can end up with a contract with no default admin.
