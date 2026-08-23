---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-27-cyfrin-majority-protocol-v2-0-3-5
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-01-27T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-27-cyfrin-majority-protocol-v2-0
title: '`DepositManager::sponsorGame` should revert if the game is `Cancelled` or
  `Concluded`'
vuln_class: []
---

# `DepositManager::sponsorGame` should revert if the game is `Cancelled` or `Concluded`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-27-cyfrin-majority-protocol-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md)_

---

**Description:** `DepositManager::sponsorGame` doesn't verify the state of the game when accepting sponsorship amounts:
```solidity
function sponsorGame(uint256 gameId, uint256 amount) external {
    GamePool storage pool = gamePools[gameId];
    pool.totalCollectedAmount += amount;
    sponsorAmounts[msg.sender][gameId] += amount;
    emit GameSponsored(gameId, msg.sender, pool.token, amount);
    SafeERC20.safeTransferFrom(IERC20(pool.token), msg.sender, address(this), amount);
}
```

**Impact:** Sponsors can sponsor `Cancelled` or `Concluded` games; in the case of `Concluded` games there is no way to retrieve their tokens. Sponsors can also sponsor non-existent games since `gameId` is not validated to belong to an actual game at all.

**Recommended Mitigation:** `DepositManager::sponsorGame` should revert if the game is `Cancelled` or `Concluded`.

**Majority Games:**
Fixed in commit [e01a1df](https://github.com/Engage-Protocol/engage-protocol/commit/e01a1df84bf8dc1cfda40ef9a52ac7bcc5e6fc75) - only allowing sponsorships for existing games in the `Created` or `Ongoing` state.

**Cyfrin:** Verified.
