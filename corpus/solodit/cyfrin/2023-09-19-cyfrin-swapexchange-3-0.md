---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-19-cyfrin-swapexchange-3-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-09-19T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-swapexchange.md
tags:
- firm:cyfrin
- report:2023-09-19-cyfrin-swapexchange
title: Using bools for storage incurs overhead
vuln_class: []
---

# Using bools for storage incurs overhead

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-19-cyfrin-swapexchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-swapexchange.md)_

---

Use uint256(1) and uint256(2) for true/false to avoid a Gwarmaccess (100 gas), and to avoid Gsset (20000 gas) when changing from `false` to `true`, after having been `true` in the past. Check more [here](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/58f635312aa21f947cae5f8578638a85aa2519f5/contracts/security/ReentrancyGuard.sol#L23-L27).

```solidity
File: helpers/FeeData.sol

18:     mapping(address => bool) public feeTokenMap;

```

```solidity
File: helpers/TransferHelper.sol

16:     bool public rewardsActive;

```

**Protocol:** Fixed in commits [2d48a4b](https://github.com/SwapExchangeio/Contracts/commit/2d48a4b7c371054207866f90b2cd98c98fb34d5a), [84dbd3a](https://github.com/SwapExchangeio/Contracts/commit/84dbd3aafa28ddad88ab1406d0946525f910a261).

**Cyfrin:** Verified.
