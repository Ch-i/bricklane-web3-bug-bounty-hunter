---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-27-cyfrin-majority-protocol-v2-0-0-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-01-27T00:00:00Z'
related_swc: []
severity: Critical
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-27-cyfrin-majority-protocol-v2-0
title: '`DepositManager::_refundEntryFee` doesn''t deduct referral rewards allowing
  users to join then leave games to drain tokens via inflated referral rewards they
  aren''t entitled to'
vuln_class: []
---

# `DepositManager::_refundEntryFee` doesn't deduct referral rewards allowing users to join then leave games to drain tokens via inflated referral rewards they aren't entitled to

_Section severity (from Solodit section header): Critical_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-27-cyfrin-majority-protocol-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md)_

---

**Description:** `DepositManager::_payEntryFee` increments the referral rewards for the user's referrer:
```solidity
referralRewards[gameId][Registry(registry).referrers(player)] += pool.ticketPrice * REFERRER_FEE;
```

But `DepositManager::_refundEntryFee` doesn't deduct referral rewards when a user leaves the game and their fee is refunded.

**Impact:** Malicious users can intentionally join then leave rescheduled games to drain tokens from the contract via inflated referral rewards they aren't entitled to.

This bug can also occur naturally without malicious users simply by users joining then leaving, giving referrers more reward allocation than they are entitled to. Once the game ends and referrers claim their inflated rewards, there will not be enough tokens to distribute to winners or for creator / protocol fees.

**Recommended Mitigation:** `DepositManager::_refundEntryFee` should deduct from the referral rewards when refunding the game fee, opposite to how `_payEntryFee` adds to the referral rewards when receiving the game fee.

**Majority Games:**
Fixed in commit [50a1e6b](https://github.com/Engage-Protocol/engage-protocol/commit/50a1e6bb3a48a6056cbf0678030be0e9424ba052).

**Cyfrin:** Verified.
