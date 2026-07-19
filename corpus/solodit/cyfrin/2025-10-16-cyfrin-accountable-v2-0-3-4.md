---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-16-cyfrin-accountable-v2-0-3-4
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-10-16T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-16-cyfrin-accountable-v2-0
title: Deployment script requires unencrypted private key
vuln_class: []
---

# Deployment script requires unencrypted private key

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-16-cyfrin-accountable-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md)_

---

**Description:** The deployment scripts [`FactoryScript.s.sol`](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/script/FactoryScript.s.sol) and [`FeeManagerScript.s.sol`](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/script/FeeManagerScript.s.sol) requires a private key to be stored in clear text as an environment variable:

```solidity
uint256 deployerPk = vm.envUint("DEPLOYER_TESTNET_PK");
```

Storing private keys in plain text represents an operational security risk, as it increases the chance of accidental exposure through version control, misconfigured backups, or compromised developer machines.

A more secure approach is to use Foundry’s [wallet management features](https://getfoundry.sh/forge/reference/script/), which allow encrypted key storage. For example, a private key can be imported into a local keystore using [`cast`](https://getfoundry.sh/cast/reference/wallet/import/):

```bash
cast wallet import deployerKey --interactive
```

This key can then be referenced securely during deployment:

```bash
forge script script/Deploy.s.sol:DeployScript \
    --rpc-url "$RPC_URL" \
    --broadcast \
    --account deployerKey \
    --sender <address associated with deployerKey> \
    -vvv
```
And used just with `vm.startBroadcast()`:
```solidity
vm.startBroadcast();

...

vm.stopBroadcast();
```

For additional guidance, see [this explanation video](https://www.youtube.com/watch?v=VQe7cIpaE54) by Patrick.

**Accountable:** Fixed in commit [`79d8cfd`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/79d8cfd8dee652adb0964ade05280a745cedb3b3)

**Cyfrin:** Verified. Deploy scripts now don't require a private key in clear text.

\clearpage
