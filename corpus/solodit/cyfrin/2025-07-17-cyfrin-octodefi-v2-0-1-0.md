---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-17-cyfrin-octodefi-v2-0-1-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-07-17T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-17-cyfrin-octodefi-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-17-cyfrin-octodefi-v2-0
title: Fee calculations break when token decimals are different from 18
vuln_class: []
---

# Fee calculations break when token decimals are different from 18

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-17-cyfrin-octodefi-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-17-cyfrin-octodefi-v2.0.md)_

---

**Description:** `FeeController.calculateFee()` and `calculateTokenAmount()` implicitly treat every ERC-20 as if it had **18 decimals**, but many popular assets (USDC/USDT = 6, etc.) do not.
Inside `calculateFee` the line

```solidity
uint256 _feeInUSD = _feeAmount * _tokenPrice / 10**18;
```

divides by `1e18` to cancel the **oracle’s** 18-dec scaling, but completely ignores the token’s own decimals. When the token has fewer decimals the resulting “USD value” is shrunk by `10**(18-decimals)`; when it has more decimals it is bloated.

Because `_executeStep()` **adds** the individual action fees returned by `_executeAction()`, any step that mixes tokens of different precision sums numbers that are not expressed in the same unit:

| Token | Decimals | Fee for $100 volume at 1 % (expected $1 = 1e18) | Fee actually returned |
|-------|----------|-----------------------------------------------|-----------------------|
| USDT  | 6        | `1 × 10¹⁸`                                    | `1 × 10⁶` (1 e12 × too low) |
| DAI   | 18       | `1 × 10¹⁸`                                    | `1 × 10¹⁸` (correct) |

When a strategy step executes an action in USDT followed by an action in DAI the total fee becomes:

```
total = 1e6  (USDT)  + 1e18 (DAI)  = 1000000000001000000  wei-USD
```

but the **semantically correct** amount should be `2 × 10¹⁸`. Down-stream effects:



**Impact:** * `StrategyBuilderPlugin.executeAutomation()` compares the aggregated fee against the user-supplied `maxFeeInUSD`. A user can set `maxFeeInUSD = 1.1e18` and still execute both actions (paying the DAI part only) because the mis-scaled USDT fee barely moves the total.
* The executor misses on revenue on every 6/8/12-dec token; conversely users of exotic high-decimal tokens may be over-charged and see their automations revert with `FeeExceedMaxFee()`.

**Recommended Mitigation:**
1. **Use token.decimals() instead of 18.**
   ```solidity
   uint8 decimals = IERC20Metadata(token).decimals();   // OZ ERC20Metadata
   uint256 scale = 10 ** decimals;                      // token’s native unit

   // feeAmount is already in token-units
   uint256 _feeInUSD = _feeAmount * _tokenPrice / scale;  // always 18-dec USD
   ```

2. **Likewise in `calculateTokenAmount()`**
   ```solidity
   uint8 decimals = IERC20Metadata(token).decimals();
   uint256 scale = 10 ** decimals;
   return feeInUSD * scale / tokenPrice;
   ```

**OctoDeFi:** Fixed in PR [\#13](https://github.com/octodefi/strategy-builder-plugin/pull/13).

**Cyfrin:** To normalize the fee in USD to the oracle decimals (18), the token decimals should be divided out in both instances. Also consider using a `staticcall` to query the token decimals and fall back to 18 if it fails.

**OctoDeFi:** Fixed in PR [\#27](https://github.com/octodefi/strategy-builder-plugin/pull/27).

**Cyfrin:** Verified. The fee amount is first normalized to 18 decimals and then divided by the oracle decimals. While this is a little more convoluted than necessary given that the oracle price is in 18 already decimals, given that the fee calculation could have simply been divided by the token decimals instead of oracle decimals without first normalizing the fee to 18 decimals, it is now correct.
