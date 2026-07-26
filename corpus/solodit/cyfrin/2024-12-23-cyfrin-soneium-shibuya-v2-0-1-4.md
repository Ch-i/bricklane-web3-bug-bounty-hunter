---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-23-cyfrin-soneium-shibuya-v2-0-1-4
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-12-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-23-cyfrin-soneium-shibuya-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-23-cyfrin-soneium-shibuya-v2-0
title: Parameter naming inconsistency
vuln_class: []
---

# Parameter naming inconsistency

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-23-cyfrin-soneium-shibuya-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-23-cyfrin-soneium-shibuya-v2.0.md)_

---

**Description:** The parameter name 'minAndBurner' in the `grantMintAndBurnRoles()` function has a typo.

```solidity
function grantMintAndBurnRoles(address minAndBurner)
```

**Recommended Mitigation:** Correct the parameter name to 'mintAndBurner'.

**Startale:** Fixed in commit [669197](https://github.com/StartaleLabs/ccip-contracts-registration/commit/669197f945405f9805e90cc6fe49552c5f6e037a).

**Cyfrin:** Verified.


\clearpage
