---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-20-cyfrin-metamask-veda-adapter-v2-0-1-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-04-20T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-20-cyfrin-metamask-veda-adapter-v2.0.md
tags:
- firm:cyfrin
- report:2026-04-20-cyfrin-metamask-veda-adapter-v2-0
title: Deployment script uses hardcoded zero-address placeholders instead of environment
  variables
vuln_class: []
---

# Deployment script uses hardcoded zero-address placeholders instead of environment variables

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-20-cyfrin-metamask-veda-adapter-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-20-cyfrin-metamask-veda-adapter-v2.0.md)_

---

**Description:** `DeployVedaAdapter.s.sol` hardcodes all four constructor parameters as `address(0)` constants (lines 19-22), requiring Solidity source code modification before each deployment. This contrasts with other scripts in the same repository that use `vm.envAddress`. The `VedaAdapter` constructor will revert if deployed with these zero addresses, but requiring source code modification increases the risk of deploying a stale version or invalidating CREATE2 address predictions.

**Recommended Mitigation:** Use `vm.envAddress` for constructor parameters, consistent with other deployment scripts in the repository:

```solidity
address owner = vm.envAddress("OWNER");
address delegationManager = vm.envAddress("DELEGATION_MANAGER");
address boringVault = vm.envAddress("BORING_VAULT");
address vedaTeller = vm.envAddress("VEDA_TELLER");
```

**MetaMask:** Fixed in commit [`57b5b88`](https://github.com/MetaMask/delegation-framework/pull/166/changes/57b5b88c10f5a5a64163f084c2c97532a11f63b7)

**Cyfrin:** Verified.


\clearpage
