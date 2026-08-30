---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-19-cyfrin-stakepet-3-4
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-09-19T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-stakepet.md
tags:
- firm:cyfrin
- report:2023-09-19-cyfrin-stakepet
title: Use shift Right/Left instead of division/multiplication if possible
vuln_class: []
---

# Use shift Right/Left instead of division/multiplication if possible

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-19-cyfrin-stakepet.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-stakepet.md)_

---

```solidity
File: StakePet.sol

420:         if (_totalValueWantsClosedown <= totalValue() / 2) {

```

**Client:** Fixed in [540cca1](https://github.com/Ranama/StakePet/commit/540cca16669ee8575806d0f3430723726e3d9c2e)

**Cyfrin:** Verified.
