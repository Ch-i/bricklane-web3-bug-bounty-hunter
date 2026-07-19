---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-01-cyfrin-licredity-v2-0-3-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-09-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-01-cyfrin-licredity-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-01-cyfrin-licredity-v2-0
title: Deployment script requires unencrypted private key
vuln_class: []
---

# Deployment script requires unencrypted private key

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-01-cyfrin-licredity-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-01-cyfrin-licredity-v2.0.md)_

---

**Description:** The deployment script [`deploy.sh`](https://github.com/Licredity/licredity-v1-core/blob/e8ae10a7d9f27529e39ca277bf56cef01a807817/deploy.sh#L29-L44) requires a private key to be stored in clear text inside the `.env` file:

```bash
# Load environment variables
source .env

...

if [ -z "$PRIVATE_KEY" ]; then
    echo "Error: PRIVATE_KEY not set in .env file"
    exit 1
fi
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

For additional guidance, see [this explanation video](https://www.youtube.com/watch?v=VQe7cIpaE54) by Patrick.

**Licredity:** Acknowledged. But won't fix here as our plan is to create a separate repo specifically for coordinating deployment and initialization, for all core / oracle / periphery. Will implement more secure practice then
