---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-25-cyfrin-myriad-v2-0-0-5
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-07-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-25-cyfrin-myriad-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-25-cyfrin-myriad-v2-0
title: Consider adding share-based sell function to avoid dust shares
vuln_class: []
---

# Consider adding share-based sell function to avoid dust shares

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-25-cyfrin-myriad-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-25-cyfrin-myriad-v2.0.md)_

---

**Description:** The current interface requires users to specify the desired amount out (tokens) when selling shares, rather than the amount in (shares to sell). This makes it difficult for users or integrators to accurately sell all their shares, especially when prices fluctuate during execution.

In many cases, users must first compute how many tokens they will receive for their full share balance using a view function like `calcSellAmount()`. However, due to price sensitivity and dynamic pool state, this off-chain calculation may become outdated by the time the transaction is submitted.

**Impact:** Because users cannot sell an exact number of shares, they will likely end up with small leftover dust balances in their accounts. This dust often isn't worth the gas to sell or claim, making it effectively unrecoverable and cluttering user balances over time.

**Recommended Mitigation:** Consider adding a new function such as:

```solidity
function sellShares(uint256 marketId, uint256 outcome, uint256 shareAmount, uint256 minAmountOut) external;
```

This would allow users to directly sell a specified number of shares, eliminating off-chain estimation errors and preventing leftover dust.

**Myriad:** Acknowledged. This makes total sense and we would love to have this option, but sadly it's too complex to implement on a smart contract.

In order to preserve the fixed product market maker formula `(L^n = O₁ * O₂ * ... * On)`, where `L` is the liquidity, `n` is the number of outcomes and `Ox` is the number of shares of outcome `x`, the formula to calculate the amount to be sold in a binary outcome would be the following:

```
// x = token amount user will receive
// shares = shares sold
// S = sell token pool balance
// O = other outcome pool balance

x² - x * (O + S + shares) + shares * O = 0
=> x = 1/2 (-sqrt(O^2 - 2 O (shares + S) + 4 * O * S + (shares + S)^2) + O + shares + S)
```

For a ternary outcome market, it would be a cubic formula:
```
x³ - x²(shares + S + O₁ + O₂) + x((shares + S)(O₁ + O₂) + O₁O₂) - shares × O₁ × O₂ = 0
```

And so on. The higher the number of outcomes, the more complex the arithmetic expression is. Calculating these is extremely gas-expensive and inaccurate to compute on a smart contract.

The alternative is the method we already have in place - do an offchain estimate of how much are the user's tokens worth, using the Newton-Raphson method, and calling `sell` with the amount returned from the method.

\clearpage
