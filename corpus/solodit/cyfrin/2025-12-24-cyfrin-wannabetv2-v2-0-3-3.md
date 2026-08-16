---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-wannabetv2-v2-0-3-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-wannabetv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-wannabetv2-v2-0
title: Use `type(uint256).max` when withdrawing from Aave
vuln_class: []
---

# Use `type(uint256).max` when withdrawing from Aave

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-wannabetv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-wannabetv2-v2.0.md)_

---

**Description:** When unwinding Aave positions in `Bet::resolve` and `cancel`, the contract withdraws using the current aToken balance as the `amount` parameter:
```solidity
uint256 aTokenBalance = IERC20(_aavePool.getReserveAToken(b.asset))
    .balanceOf(address(this));
_aavePool.withdraw(b.asset, aTokenBalance, address(this));
```

Aave’s [recommended pattern](https://aave.com/docs/aave-v3/smart-contracts/pool?utm_source=chatgpt.com#write-methods-withdraw) for fully closing a position is to pass `type(uint256).max`, which is more robust against rounding/indexing edge cases. This also removes one external call as `withdraw` returns the amount withdrawn:
```solidity
uint256 aTokenBalance = _aavePool.withdraw(b.asset, type(uint256).max, address(this));
```

**WannaBet:** Fixed in commit [b060cf6](https://github.com/gskril/wannabet-v2/commit/b060cf65724fc00d54b6440454261f63d662cc57).

**Cyfrin:** Verified.
