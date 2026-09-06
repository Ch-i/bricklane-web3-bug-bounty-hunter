---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-21-cyfrin-illuvium-stakingv3-v2-0-0-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-10-21T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-21-cyfrin-illuvium-stakingv3-v2-0
title: Deployment script requires unencrypted private key
vuln_class: []
---

# Deployment script requires unencrypted private key

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md)_

---

**Description:** The [Makefile](https://github.com/0xKaizenLabs/staking-contracts-v3/blob/c78653ed5f2e5a6d5ace13c303a8765fe30679b0/Makefile)’s deployment targets require a raw private key to be supplied via an environment variable and pass it directly on the command line to `forge`:

```make
# Guard (fails if PRIVATE_KEY not provided)
@if [ -z "$(PRIVATE_KEY)" ]; then \
    echo "$(RED)ERROR: PRIVATE_KEY not set$(NC)"; \
    exit 1; \
fi

# Usage (Sepolia)
forge script script/Deployer.s.sol:Deployer \
  --rpc-url $(BASE_SEPOLIA_RPC) \
  --private-key $(PRIVATE_KEY) \
  --broadcast \
  --verify \
  --etherscan-api-key $(BASESCAN_API_KEY) \
  -vvvv

# Usage (Mainnet)
forge script script/Deployer.s.sol:Deployer \
  --rpc-url $(BASE_RPC) \
  --private-key $(PRIVATE_KEY) \
  --broadcast \
  --verify \
  --etherscan-api-key $(BASESCAN_API_KEY) \
  --slow \
  -vvvv
```

Supplying secrets this way encourages plaintext handling (e.g., `.env` files, shell history) and exposes the key in process arguments. Storing private keys in plain text represents an operational security risk, as it increases the chance of accidental exposure through version control, misconfigured backups, or compromised developer machines.

A more secure approach is to use Foundry’s [wallet management features](https://getfoundry.sh/forge/reference/script/), which allow encrypted key storage. For example, a private key can be imported into a local keystore using [`cast`](https://getfoundry.sh/cast/reference/wallet/import/):

```bash
cast wallet import deployerKey --interactive
```

This key can then be referenced securely during deployment:

```make
DEPLOYER_ACCOUNT ?= deployerKey
DEPLOYER_SENDER  ?= $(shell cast wallet address $(DEPLOYER_ACCOUNT) 2>/dev/null)

forge script script/Deployer.s.sol:Deployer \
  --rpc-url $(BASE_SEPOLIA_RPC) \
  --account $(DEPLOYER_ACCOUNT) \
  --sender $(DEPLOYER_SENDER) \
  --broadcast \
  --verify \
  --etherscan-api-key $(BASESCAN_API_KEY) \
  -vvvv
```
and
```make
cast wallet list | grep -q "$(DEPLOYER_ACCOUNT)" || { \
  echo "$(RED)ERROR: Keystore account '$(DEPLOYER_ACCOUNT)' not found$(NC)"; exit 1; }
```

For additional guidance, see [this explanation video](https://www.youtube.com/watch?v=VQe7cIpaE54) by Patrick.

**Illuvium:** Fixed in commit [5f273bc](https://github.com/0xKaizenLabs/staking-contracts-v3/commit/5f273bc8a196170162400c33a43efe2fb84f0013).

**Cyfrin:** Verified.
