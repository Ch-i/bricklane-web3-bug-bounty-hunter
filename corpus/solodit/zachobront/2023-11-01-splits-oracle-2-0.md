---
affected_contracts: []
derives_from: []
id: solodit-zachobront-2023-11-01-splits-oracle-2-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-11-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-splits-oracle.md
tags:
- firm:zachobront
- report:2023-11-01-splits-oracle
title: '[L-01] Rearrange stale price check formula out of absurd paranoia'
vuln_class: []
---

# [L-01] Rearrange stale price check formula out of absurd paranoia

_Section severity (from Solodit section header): Low_  
_Audit firm: ZachObront_  
_Source report: [2023-11-01-splits-oracle.md](https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-splits-oracle.md)_

---

In `_getFeedAnswer()`, we check if the Chainlink oracle has returned a stale price:
```solidity
if (updatedAt < block.timestamp - feed_.staleAfter) {
    revert StalePrice(feed_.feed, updatedAt);
}
```
`feed_.staleAfter` is a `uint24`, so for any chain that uses standard Unix timestamps, it should be impossible for `block.timestamp - feed_.staleAfter` to underflow (because the current Unix time is greater than `type(uint24).max`).

However, out of an abundance of paranoia, it is worth rearranging the formula to accomplish the same thing without risk of reverting.

**Recommendation**

```diff
- if (updatedAt < block.timestamp - feed_.staleAfter) {
+ if (updatedAt + feed_.staleAfter < block.timestamp) {
      revert StalePrice(feed_.feed, updatedAt);
  }
```

**Review**

[Fixed as recommended.](https://github.com/0xSplits/splits-oracle/commit/aeae0e2d4241d3279f2db5294d7a619b393a818c)
