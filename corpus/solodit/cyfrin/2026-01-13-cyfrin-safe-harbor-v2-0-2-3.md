---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-13-cyfrin-safe-harbor-v2-0-2-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-01-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-13-cyfrin-safe-harbor-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-13-cyfrin-safe-harbor-v2-0
title: Inconsistencies in names and data types between legal agreement and smart contracts
vuln_class: []
---

# Inconsistencies in names and data types between legal agreement and smart contracts

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-13-cyfrin-safe-harbor-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-13-cyfrin-safe-harbor-v2.0.md)_

---

**Description:** The legal agreement (Section 1.1(c)) specifies the `DAO Adoption Procedures` must call `adoptSafeHarbor` on `SafeHarborRegistryV2.sol` deployed at `0x1eaCD100B0546E433fbf4d773109cAD482c34686`, setting an `AgreementDetailsV2` struct.

The current implementation diverges in the following ways:

Component | Legal Agreement | Implementation
-- | -- | --
Registry Contract | SafeHarborRegistryV2.sol | SafeHarborRegistry.sol
Version | V2 (implied) | VERSION = "3.0.0"
Details Struct | AgreementDetailsV2 | AgreementDetails


There is also a difference in naming of variables:
Legal Agreement (section 1.1.c)  | Implementation | Location
-- | -- | --
chainID|caip2ChainId| `Chain` struct
`identityRequirement`| `identity` | `BountyTerms` struct

There is a type naming difference:
Legal Agreement (section 1.1.c.iv)  | Implementation
-- | --
`identityRequirement`| `identityRequirements`


There is a type difference:
Field  | Legal agreement (section 1.1.c.iv) | Implementation
-- | -- | --
`bountPercentage`| `string`| `uint256`


**Recommended Mitigation:** Consider making the implementation consistent with the legal agreement terminology.

**SafeHarbor:**
Fixed in [0d70af3](https://github.com/PatrickAlphaC/safe-harbor/commit/0d70af3c37ff451e50bc2f2087d23d23aec7d08a).

**Cyfrin:** Verified.

\clearpage
