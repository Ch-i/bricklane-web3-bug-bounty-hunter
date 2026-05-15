---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-wannabetv2-v2-0-2-6
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-wannabetv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-wannabetv2-v2-0
title: '`BetResolved` event in `Bet::resolve` will have the wrong `totalWinnings`
  when Aave pool is used'
vuln_class: []
---

# `BetResolved` event in `Bet::resolve` will have the wrong `totalWinnings` when Aave pool is used

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-wannabetv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-wannabetv2-v2.0.md)_

---

**Description:** In `Bet::resolve`, `BetResolved` is emitted with `totalWinnings = makerStake + takerStake` before checking the actual funds in Aave and capping `totalWinnings` to the contract’s `aTokenBalance`:
```solidity
uint256 totalWinnings = b.makerStake + b.takerStake;
emit BetResolved(winner, totalWinnings);

// If the funds are in Aave, withdraw them
if (address(_aavePool) != address(0)) {
    uint256 aTokenBalance = IERC20(_aavePool.getReserveAToken(b.asset)).balanceOf(address(this));

    // @audit totalWinnings changed
    totalWinnings = _min(totalWinnings, aTokenBalance);
    _aavePool.withdraw(b.asset, aTokenBalance, address(this));
}
```

When an Aave pool is used (with yield or loss), the event’s `amount` field may not match the actual winnings transferred to the `winner`, making the event misleading for indexers and off-chain consumers.

Consider emitting the event after the Aave accounting has been applied.

**WannaBet:** Fixed as of commit [c18aae0](https://github.com/gskril/wannabet-v2/commit/c18aae04ef570ef877f7d06aa25ca6f10a379fc1).

**Cyfrin:** Verified.
