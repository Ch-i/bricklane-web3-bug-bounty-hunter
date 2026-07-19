---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-19-cyfrin-swapexchange-3-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-09-19T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-swapexchange.md
tags:
- firm:cyfrin
- report:2023-09-19-cyfrin-swapexchange
title: Cache array length outside of loop
vuln_class: []
---

# Cache array length outside of loop

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-19-cyfrin-swapexchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-swapexchange.md)_

---

If not cached, the solidity compiler will always read the length of the array during each iteration. That is, if it is a storage array, this is an extra sload operation (100 additional extra gas for each iteration except for the first) and if it is a memory array, this is an extra mload operation (3 additional gas for each iteration except for the first).

```solidity
File: SwapExchange.sol

403:         for (uint i = 0; i < swapIds.length; i++) {
```

```solidity
File: helpers/FeeData.sol

55:         for (uint i = 0; i < feeTokenAddresses.length; i++) {
61:         for (uint i = 0; i < feeTokenKeys.length; i++) {

```

**Protocol:** Fixed in commit [9ba2a93](https://github.com/SwapExchangeio/Contracts/commit/9ba2a93bdad911f541056ced4661bb2fce8db8e0)

**Cyfrin:** Verified.
