---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-27-cyfrin-majority-protocol-v2-0-4-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-01-27T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-27-cyfrin-majority-protocol-v2-0
title: Perform storage updates prior to external calls
vuln_class: []
---

# Perform storage updates prior to external calls

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-27-cyfrin-majority-protocol-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md)_

---

**Description:** Most times it is safer to perform storage updates prior to external calls:
* `DepositManager.sol`
```solidity
// switch these around in `_refundEntryFee`
186:        SafeERC20.safeTransfer(IERC20(pool.token), player, pool.ticketPrice);
187:        pool.totalCollectedAmount -= pool.ticketPrice;
```

* `SessionManager.sol`
```solidity
// in `joinGame` perform the 2 storage updates prior to calling `_payEntryFee`
311:        _payEntryFee(_gameId, msg.sender);
312:        contestants[_gameId][msg.sender] = true;
313:        games[_gameId].numContestants++;
```

**Majestic Games:**
Fixed in commit [6525ee1](https://github.com/Engage-Protocol/engage-protocol/commit/6525ee1547e0b7834cb99a786773bed1861369c7).

**Cyfrin:** Verified.
