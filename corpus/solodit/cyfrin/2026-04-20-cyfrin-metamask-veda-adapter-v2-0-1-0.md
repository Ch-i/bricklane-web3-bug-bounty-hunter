---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-20-cyfrin-metamask-veda-adapter-v2-0-1-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-04-20T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-20-cyfrin-metamask-veda-adapter-v2.0.md
tags:
- firm:cyfrin
- report:2026-04-20-cyfrin-metamask-veda-adapter-v2-0
title: Deployment script instructs using plaintext private key via CLI argument
vuln_class: []
---

# Deployment script instructs using plaintext private key via CLI argument

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-20-cyfrin-metamask-veda-adapter-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-20-cyfrin-metamask-veda-adapter-v2.0.md)_

---

**Description:** The deployment script `DeployVedaAdapter.s.sol` documents usage with `--private-key $PRIVATE_KEY`, instructing deployers to pass the private key as a plaintext CLI argument sourced from an environment variable. The `.env.example` file contains a `PRIVATE_KEY=` entry confirming this pattern. While `.gitignore` covers `*.env` files, the key is still exposed in shell history, process listings, and CI logs.

**Recommended Mitigation:** Migrate to Foundry's encrypted keystore:

```bash
cast wallet import deployer --interactive
forge script script/DeployVedaAdapter.s.sol --rpc-url <rpc_url> --account deployer --broadcast
```

Update the NatSpec in the deployment script to document this secure pattern. Remove `PRIVATE_KEY` from `.env.example`.

**MetaMask:** Noted.
