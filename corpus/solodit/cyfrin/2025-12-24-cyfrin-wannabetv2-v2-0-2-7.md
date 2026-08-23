---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-wannabetv2-v2-0-2-7
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-wannabetv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-wannabetv2-v2-0
title: Taker receives Aave yield for cancelled pending bets
vuln_class: []
---

# Taker receives Aave yield for cancelled pending bets

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-wannabetv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-wannabetv2-v2.0.md)_

---

**Description:** If a bet uses an Aave pool but never becomes `ACTIVE` (taker never accepts), only the maker’s stake is supplied to Aave. In `Bet::cancel`, the recovered Aave balance is still split using maker/taker logic:
```solidity
uint256 aTokenBalance = IERC20(_aavePool.getReserveAToken(b.asset))
    .balanceOf(address(this));
_aavePool.withdraw(b.asset, aTokenBalance, address(this));

makerRefund = _min(makerRefund, aTokenBalance);
takerRefund = _min(takerRefund, aTokenBalance - makerRefund);
```

So the taker can receive part of the maker’s accrued yield (or recovered principal) despite never having deposited. However this is balanced out by the maker having priority to be refunded, if for example there was a "negative yield" event in Aave which caused the total amount withdrawn from Aave to be less than what was deposited.

Consider whether:
1) the treasury should receive any Aave generated yield when the bet is cancelled
2) if the taker never accepted, whether they should still receive Aave yield

**WannaBet:** Fixed in commit [f1750a9](https://github.com/gskril/wannabet-v2/commit/f1750a975346b1472ef3306db31f6fc7bd2db3b5) such that:
* taker only receives refund if they deposited
* yield is sent either to treasury if it exists or otherwise to the maker

**Cyfrin:** Verified.
