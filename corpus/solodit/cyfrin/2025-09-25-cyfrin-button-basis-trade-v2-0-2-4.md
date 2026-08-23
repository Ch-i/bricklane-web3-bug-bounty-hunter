---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-25-cyfrin-button-basis-trade-v2-0-2-4
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-09-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-25-cyfrin-button-basis-trade-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-25-cyfrin-button-basis-trade-v2-0
title: Deployment script requires unencrypted private keys
vuln_class: []
---

# Deployment script requires unencrypted private keys

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-25-cyfrin-button-basis-trade-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-25-cyfrin-button-basis-trade-v2.0.md)_

---

**Description:** Several deployment/ops scripts require private keys to be loaded from environment variables and used directly inside the script, e.g.:

```solidity
// DeployBasisTradeTailor.s.sol
uint256 deployerPrivateKey = vm.envUint("DEPLOYER_PRIVATE_KEY");
uint256 adminPrivateKey    = vm.envUint("ADMIN_PRIVATE_KEY");
...
vm.startBroadcast(deployerPrivateKey);
...
vm.startBroadcast(adminPrivateKey);

// DeployBasisTradeVault.s.sol
uint256 deployerPrivateKey = vm.envUint("DEPLOYER_PRIVATE_KEY");
...
vm.startBroadcast(deployerPrivateKey);

// DeployMockPocketOracle.s.sol
uint256 deployerPrivateKey = vm.envUint("DEPLOYER_PRIVATE_KEY");
...
vm.startBroadcast(deployerPrivateKey);

// DeployMocks.s.sol
uint256 deployerPrivateKey = vm.envUint("DEPLOYER_PRIVATE_KEY");
...
vm.startBroadcast(deployerPrivateKey);
```

Storing and loading raw private keys via `.env` (plain text) is an operational security risk: keys can be leaked through version control, logs, shell history, misconfigured backups, or compromised developer machines/CI runners.

A safer approach is to avoid embedding keys in scripts and use Foundry’s [wallet management](https://getfoundry.sh/forge/reference/script/) and keystore support. Recommended pattern:

1. Import keys into an encrypted local keystore (once per machine) using [`cast`](https://getfoundry.sh/cast/reference/wallet/import/):

```bash
cast wallet import deployerKey --interactive
cast wallet import adminKey --interactive
cast wallet import agentKey --interactive   # if needed
```

2. Change scripts to use parameterless broadcasting so the signer is supplied by CLI:

```solidity
// before: vm.startBroadcast(deployerPrivateKey);
vm.startBroadcast();
// ...
vm.stopBroadcast();
```

3. Run each role-sensitive phase as the appropriate account (split into separate runs or separate scripts if different signers are required):

```bash
# Deployer phase
forge script script/DeployBasisTradeTailor.s.sol:DeployBasisTradeTailor \
  --rpc-url "$RPC_URL" --broadcast --account deployerKey --sender <deployer_addr> -vvv

# Admin phase (grants/approvals)
forge script script/ConfigureBasisTradeTailor.s.sol:ConfigureBasisTradeTailor \
  --rpc-url "$RPC_URL" --broadcast --account adminKey --sender <admin_addr> -vvv
```

This keeps private keys encrypted at rest and never exposes them via plaintext environment variables. As alternatives, consider hardware wallets (`--ledger`), and ensure `.env` never contains raw keys in shared environments.

For additional guidance, see [this explanation video](https://www.youtube.com/watch?v=VQe7cIpaE54) by Patrick.

**Button:** Fixed in commit [`c89bce0`](https://github.com/buttonxyz/button-protocol/commit/c89bce0f88770f473524e997eb47fca7dccae0e0)

**Cyfrin:** Verified. Keystores are now used for the keys.
