---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-19-cyfrin-swapexchange-3-6
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-09-19T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-swapexchange.md
tags:
- firm:cyfrin
- report:2023-09-19-cyfrin-swapexchange
title: Use != 0 instead of > 0 for unsigned integer comparison
vuln_class: []
---

# Use != 0 instead of > 0 for unsigned integer comparison

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-19-cyfrin-swapexchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-swapexchange.md)_

---

```solidity
File: helpers/FeeData.sol

64:         while (feeTokenKeys.length > 0) {

```

```solidity
File: libraries/SwapUtils.sol

96:         else if (sentAmount > 0) {

```

**Protocol:** Fixed in commit [4679de1](https://github.com/SwapExchangeio/Contracts/commit/4679de1c3f8adfc4122698fc82a529322ba4b5ed).

**Cyfrin:** Verified.
