---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-12-cyfrin-molecule-onchainlab-v2-0-4-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-05-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-12-cyfrin-molecule-onchainlab-v2-0
title: 'NatSpec error in `OnChainLab::initialize`: `setRegistry` is not ''Module Registry'''
vuln_class: []
---

# NatSpec error in `OnChainLab::initialize`: `setRegistry` is not 'Module Registry'

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-12-cyfrin-molecule-onchainlab-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md)_

---

**Description:** The comment "Set the Module Registry" precedes a call to `setRegistry(IERC7484Registry(_registry), attesters, threshold)`, which configures the ERC-7484 attestation registry - a *trust* registry, not a "module registry." The two are distinct: a module registry would enumerate installed modules; ERC-7484 is an attestation feed. The comment misnames the responsibility.

```solidity
src/OnChainLab.sol
153:        // Set the Module Registry
154:        setRegistry(IERC7484Registry(_registry), attesters, threshold);
```

**Recommended Mitigation:**
```solidity
// Configure the ERC-7484 attestation registry and trusted attesters.
setRegistry(IERC7484Registry(_registry), attesters, threshold);
```

**Molecule:** Fixed in commit [3f6f24e](https://github.com/moleculeprotocol/onchainlabs/commit/3f6f24e).

**Cyfrin:** Verified.
