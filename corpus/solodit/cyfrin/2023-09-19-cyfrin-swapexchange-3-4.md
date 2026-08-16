---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-19-cyfrin-swapexchange-3-4
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
title: Don't initialize variables with default value
vuln_class: []
---

# Don't initialize variables with default value

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

```solidity
File: libraries/Constants.sol

6:     uint8 public constant FEE_TYPE_ETH_FIXED = 0;

```

**Protocol:** Fixed for for-loops in commit 83ffebcc099da256ec53644afc733eab2586c636.

**Cyfrin:** Verified.
