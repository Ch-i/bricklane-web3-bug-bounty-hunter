---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-19-cyfrin-swapexchange-3-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-09-19T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-swapexchange.md
tags:
- firm:cyfrin
- report:2023-09-19-cyfrin-swapexchange
title: For Operations that will not overflow, you could use unchecked
vuln_class: []
---

# For Operations that will not overflow, you could use unchecked

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-19-cyfrin-swapexchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-swapexchange.md)_

---

```solidity
File: SwapExchange.sol

209:    ++recordCount;

254:    totalNativeSendAmount += calculation.nativeSendAmount;

407:    total += swap.amountA;

```

```solidity
File: libraries/SwapUtils.sol

93:             uint256 expectedValue = amount + fee;

```

**Protocol:** Fixed in commit [f7a5dac](https://github.com/SwapExchangeio/Contracts/commit/f7a5dac3141f71b06a6d4ad3e44d657bc55ee441).

**Cyfrin:** Verified.
