---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-25-cyfrin-myriad-v2-0-0-4
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-07-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-25-cyfrin-myriad-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-25-cyfrin-myriad-v2-0
title: Consider adding a `deadline` parameter to user facing calls
vuln_class: []
---

# Consider adding a `deadline` parameter to user facing calls

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-25-cyfrin-myriad-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-25-cyfrin-myriad-v2.0.md)_

---

**Description:** The `buy`, `sell`, `addLiquidity`, and `removeLiquidity` functions currently do not accept a `deadline` parameter to constrain when a transaction must be executed. Without a deadline, transactions may be mined at unexpected times, especially if there are delays in submission or relaying, leading to unexpected pricing or market state changes.

**Impact:** Transactions that execute later than intended may result in unfavorable outcomes for users, particularly in volatile or thin markets. Including a deadline improves predictability and user trust by ensuring the action is executed only within the expected time window.

**Recommended Mitigation:** Add a `uint256 deadline` parameter to user-facing functions and enforce it using a modifier:

```solidity
modifier onlyBefore(uint256 deadline) {
    require(block.timestamp <= deadline, "!d");
    _;
}
```
This ensures the transaction will revert if not mined before the user-specified deadline.


**Myriad:** Acknowledged. Even though this extra layer of verification would be helpful, I believe there are already other mechanisms in place to avoid the use cases you mention:

- Slippage is already configurable through the following:
  - `buy` - `minOutcomeSharesToBuy`
  - `sell` -  `maxOutcomeSharesToSell`
  - `addLiquidity` - `minSharesIn` (implemented in [#88](https://github.com/Polkamarkets/polkamarkets-js/pull/88))
  - `removeLiquidity` - `minValueOut` (implemented in [#88](https://github.com/Polkamarkets/polkamarkets-js/pull/88))

These configs protect users from volatility / unexpected pricing changes.

In order to prevent issues form market state changes, the `timeTransitions` modifier will act and gracefully revert the transaction without the need for a `deadline`

My main concern is mostly adding an extra layer of logic to the main functions, which would add complexity (it would require an extra argument in all functions) - when we do already mechanisms in the function arguments that prevent the mentioned issues.
