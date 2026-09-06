---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-04-cyfrin-parallel3-1-v2-0-2-3
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-03-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-04-cyfrin-parallel3-1-v2-0
title: Excess `amountStableOut` not credited during Harvest in `GenericHarvester`
vuln_class: []
---

# Excess `amountStableOut` not credited during Harvest in `GenericHarvester`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-04-cyfrin-parallel3.1-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md)_

---

**Description:** In the `GenericHarvester` contract, within the `onFlashLoan` function, there is an issue with handling the difference between the flashloaned amount and the received `amountStableOut`.

If `amountStableOut` is less than the flashloaned amount, the difference is correctly deducted from the original sender.
However, if `amountStableOut` exceeds the flashloaned amount (e.g., due to favorable swap rates or additional yields), the excess amount is not credited back to the original sender or handled appropriately.
```solidity
  function onFlashLoan(
    ...
  )
    ...
  {
    ...
    uint256 amountStableOut =
      parallelizer.swapExactInput(amountOut, minAmountOut, tokenOut, address(tokenP), address(this), block.timestamp);
    //@audit => In case there is any excess, that difference is not tracked nor send out of the contract
@>    if (amount > amountStableOut) {
      budget[sender] -= amount - amountStableOut; // Will revert if not enough funds
    }
    return CALLBACK_SUCCESS;
  }

```

**Recommended Mitigation:** Consider adding a case to handle any excess and credit it to the original sender.

**Parallel:** Acknowledged. Harvester contracts will be refactored.
