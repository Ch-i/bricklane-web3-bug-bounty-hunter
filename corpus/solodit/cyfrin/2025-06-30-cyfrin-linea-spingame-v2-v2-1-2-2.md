---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-30-cyfrin-linea-spingame-v2-v2-1-2-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-06-30T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-30-cyfrin-linea-spingame-v2-v2.1.md
tags:
- firm:cyfrin
- report:2025-06-30-cyfrin-linea-spingame-v2-v2-1
title: Cache `prize.amount` in `SpinGame::_transferPrize`
vuln_class: []
---

# Cache `prize.amount` in `SpinGame::_transferPrize`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-30-cyfrin-linea-spingame-v2-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-30-cyfrin-linea-spingame-v2-v2.1.md)_

---

**Description:** In `SpinGame::_transferPrize`, when transferring either an ERC20 or native token prize, the `prize.amount` field is read three times: once for the `if` check, once to compare against the contract balance, and again when executing the transfer:

```solidity
if (prize.amount > 0) {
    ...
    if (contractBalance < prize.amount) {
        revert PrizeAmountExceedsBalance(..., prize.amount, contractBalance);
    }
    ...
    token.safeTransfer(_winner, prize.amount);
}
```

This results in three separate reads of the same storage slot. Since the value does not change during execution, it can be cached once.

Consider caching `prize.amount` at the head of the first if:

```solidity
uint256 amount = prize.amount;
if (amount > 0) {
    ...
    if (contractBalance < amount) {
        revert PrizeAmountExceedsBalance(..., amount, contractBalance);
    }
    ...
    token.safeTransfer(_winner, amount);
}
```

**Linea:** Fixed in commit [`0290123`](https://github.com/Consensys/linea-hub/pull/557/commits/02901233dbe9a184b80bffb67bf5d489bc015a10)

**Cyfrin:** Verified. `prize.amount` is now cached and the cached value is used.

\clearpage
