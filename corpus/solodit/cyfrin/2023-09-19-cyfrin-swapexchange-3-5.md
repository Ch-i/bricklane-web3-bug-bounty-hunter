---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-19-cyfrin-swapexchange-3-5
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
title: '`++i` costs less gas than `i++`, especially when it''s used in `for`-loops
  (`--i`/`i--` too)'
vuln_class: []
---

# `++i` costs less gas than `i++`, especially when it's used in `for`-loops (`--i`/`i--` too)

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-19-cyfrin-swapexchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-swapexchange.md)_

---

```solidity
File: SwapExchange.sol

130:         for (uint256 i = 0; i < length; i++) {

161:         for (uint256 i = 0; i < swapIdCount; i++) {

247:         for (uint256 i = 0; i < length; i++) {

346:         for (uint256 i = 0; i < swapIdCount; i++) {

403:         for (uint i = 0; i < swapIds.length; i++) {

```

```solidity
File: helpers/FeeData.sol

55:         for (uint i = 0; i < feeTokenAddresses.length; i++) {

61:         for (uint i = 0; i < feeTokenKeys.length; i++) {

```

**Protocol:** Fixed in commit [5662786](https://github.com/SwapExchangeio/Contracts/commit/5662786421251a32444427d4ede74100a4c772f0).

**Cyfrin:** Verified.
