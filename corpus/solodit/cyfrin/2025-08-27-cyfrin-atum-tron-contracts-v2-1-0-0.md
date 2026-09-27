---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-27-cyfrin-atum-tron-contracts-v2-1-0-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-08-27T00:00:00Z'
related_swc: []
severity: Critical
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-27-cyfrin-atum-tron-contracts-v2.1.md
tags:
- firm:cyfrin
- report:2025-08-27-cyfrin-atum-tron-contracts-v2-1
title: '`USDT` tokens on TRON used as deposits will be permanently stuck in `Escrow`
  contract as `Escrow::release, refund` revert due to critical bug inside USDT''s
  `transfer` function'
vuln_class: []
---

# `USDT` tokens on TRON used as deposits will be permanently stuck in `Escrow` contract as `Escrow::release, refund` revert due to critical bug inside USDT's `transfer` function

_Section severity (from Solodit section header): Critical_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-27-cyfrin-atum-tron-contracts-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-27-cyfrin-atum-tron-contracts-v2.1.md)_

---

**Description:** The official TRON USDT token address is [given](https://tron.network/usdt) as [TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t](https://tronscan.org/#/contract/TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t/code).

The relevant inheritance heirarchy is `TetherToken -> StandardTokenWithFees -> StandardToken -> BasicToken`.

There appears to be one significant bug inside `StandardTokenWithFees::transfer` which does this:
```solidity
  function transfer(address _to, uint _value) public returns (bool) {
    uint fee = calcFee(_value);
    uint sendAmount = _value.sub(fee);

    super.transfer(_to, sendAmount);
    if (fee > 0) {
      super.transfer(owner, fee);
    }
  }
```

The bug here is there is no `return` statement so this will return `false` even for successful transfers.

`TetherToken::transfer` will call this function if `deprecated == false` which is [currently the case](https://tronscan.org/#/contract/TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t/code?func=Tab-read-F2). The `transferFrom` function is fine as that has the return, it is only transfer which is the problem.

**Impact:** In Atum's codebase `Escrow::release, refund` call `safeTransfer` which under-the-hood calls `IERC20::transfer`. When `token == USDT` even using `safeTransfer` this bad bug causes the successful transfer to revert due to `StandardTokenWithFees::transfer` returning `false`. This results in escrowed USDT tokens being permanently stuck inside the `Escrow` contract.

**Recommended Mitigation:** In `Escrow::release, refund` when `token == USDT` just call `usdt.transfer` and ignore the return value - this is safe as it will always revert if the transfer failed.

**Atum:**
Fixed in commit [12fb91a](https://github.com/Atum-Labs/tvm-contracts/commit/12fb91a270e3b48639bd06fdd27d56e95893c898).

**Cyfrin:** Verified.

\clearpage
