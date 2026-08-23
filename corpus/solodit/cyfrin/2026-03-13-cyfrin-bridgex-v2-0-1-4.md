---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-bridgex-v2-0-1-4
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-bridgex-v2-0
title: Use Foundry's encrypted secure private key storage instead of plaintext environment
  variables
vuln_class: []
---

# Use Foundry's encrypted secure private key storage instead of plaintext environment variables

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-bridgex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md)_

---

**Description:** Both deployment scripts read the deployer's private key from a plaintext environment variable:

```solidity
// DeployPrivateBridge.s.sol:10
uint256 deployerKey = vm.envUint("DEPLOYER_PRIVATE_KEY");

// DeployPublicBridge.s.sol:11
uint256 deployerKey = vm.envUint("DEPLOYER_PRIVATE_KEY");
```

This requires the private key to be stored in a `.env` file or shell environment as unencrypted plaintext. Plaintext private keys are exposed through version control leaks (accidental `.env` commits), shell history, misconfigured backups, compromised developer machines, or CI/CD logs. The deployer key is particularly sensitive as it becomes the `owner` of both bridge contracts with full admin privileges (pause, set fees, add/remove releasers, force-process releases).

**Impact:**
- Deployer private key exposure compromises the owner role on all deployed bridge contracts
- Attacker with the key can pause bridges, drain fees, manipulate releasers, or force-process releases
- Risk persists after deployment since the deployer key remains the owner

**Recommended Mitigation:** Use Foundry's encrypted keystore instead of plaintext environment variables:

```bash
# Import key once (encrypted with password, stored in ~/.foundry/keystores/)
cast wallet import deployer --interactive

# Use in deployment scripts (prompts for password, key never in plaintext)
forge script script/DeployPublicBridge.s.sol --account deployer --broadcast
```

Update deployment scripts to remove the private key parameter:

```solidity
function run() external {
    // No private key in environment — Foundry decrypts from keystore at runtime
    vm.startBroadcast();
    // ... deployment logic ...
    vm.stopBroadcast();
}
```

See this Updraft [lesson](https://updraft.NerdUnited-NodeGovernance.io/courses/foundry/foundry-simple-storage/never-use-a-env-file) on using Foundry's encrypted secure private key storage.

**BridgeX:**
Fixed in commit [caf269f](https://github.com/NerdUnited-NodeGovernance/bridge-x-contracts/commit/caf269f05feaff8b9c6ee8003b871d3d70e0ffc4).

**Cyfrin:** Verified.
