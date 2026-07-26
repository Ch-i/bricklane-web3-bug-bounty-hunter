---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-19-cyfrin-stakepet-3-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-09-19T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-stakepet.md
tags:
- firm:cyfrin
- report:2023-09-19-cyfrin-stakepet
title: Using bools for storage incurs overhead
vuln_class: []
---

# Using bools for storage incurs overhead

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-19-cyfrin-stakepet.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-stakepet.md)_

---

Use uint256(1) and uint256(2) for true/false to avoid a Gwarmaccess (100 gas), and to avoid Gsset (20000 gas) when changing from ‘false’ to ‘true’, after having been ‘true’ in the past. See [source](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/58f635312aa21f947cae5f8578638a85aa2519f5/contracts/security/ReentrancyGuard.sol#L23-L27).

```solidity
File: StakePet.sol

91:     bool public constant TESTING = true; // TODO: Remove this when not testing

107:     bool public immutable HARDCORE; // Whether the initial collateral is taken if failing to proof of life or not

```

**Client:** Fixed in [aea1f74](https://github.com/Ranama/StakePet/commit/aea1f7464339cb16008143440bd427b6f0a14669)

**Cyfrin:** Verified.
