---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-19-cyfrin-swapexchange-2-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-09-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-swapexchange.md
tags:
- firm:cyfrin
- report:2023-09-19-cyfrin-swapexchange
title: Unnecessary logical operation
vuln_class: []
---

# Unnecessary logical operation

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-19-cyfrin-swapexchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-swapexchange.md)_

---

**Severity:** Informational

**Description:** In the function `SwapExchange::calculateMultiSwap()` there is a logical operation that is not necessary in the for loop.

```solidity
SwapExchange.sol
161:         for (uint256 i = 0; i < swapIdCount; i++) {
162:             swapId = multiClaimInput.swapIds[i];
163:             SwapUtils.Swap memory swap = swaps[swapId];
164:             if (swap.tokenB != matchToken) revert Errors.NonMatchingToken();
165:             if (swap.amountB < matchAmount) revert Errors.NonMatchingAmount();
166:             if (matchAmount < swap.amountB) {
167:                 if (!swap.isPartial) revert Errors.NotPartialSwap();
168:                 matchAmount = MathUtils._mulDiv(swap.amountA, matchAmount, swap.amountB);
169:                 complete = complete && false;//@audit-issue INFO unnecessary operation, just set complete=false
170:             }
171:             else {
172:                 matchAmount = swap.amountA;
173:             }
174:             matchToken = swap.tokenA;
175:         }
```

**Protocol:** Fixed in commit [a079c11](https://github.com/SwapExchangeio/Contracts/commit/a079c11cc3bc044c61493040dab1f94de4a0f14a).

**Cyfrin:** Verified.
