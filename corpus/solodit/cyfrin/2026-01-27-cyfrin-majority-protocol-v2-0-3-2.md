---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-27-cyfrin-majority-protocol-v2-0-3-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-01-27T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-27-cyfrin-majority-protocol-v2-0
title: Referral rewards accumulate to `address(0)` when players aren't referred
vuln_class: []
---

# Referral rewards accumulate to `address(0)` when players aren't referred

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-27-cyfrin-majority-protocol-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md)_

---

**Description:** `DepositManager::_payEntryFee` does this:
```solidity
referralRewards[gameId][Registry(registry).referrers(player)] += pool.ticketPrice * REFERRER_FEE;
```

But `Registry(registry).referrers(player)` returns `address(0)` when `player` has not been referred.

**Impact:** Referral rewards accumulate to `address(0)`. These can't be claimed but it is still incorrect and should be fixed.

**Recommended Mitigation:** Only allocate referral rewards if the player has actually been referred; eg if `Registry(registry).referrers(player) != address(0)`.

**Majority Games:**
Fixed in commit [e090f2e](https://github.com/Engage-Protocol/engage-protocol/commit/e090f2e1b5f42eb212fdbda7be94ccf295281075) by introducing a `CLAIMER_ROLE` which can collect referral fees assigned to `address(0)`, such that referral fees are always collected. `Registry::setReferrer` has been modified to prevent an address having `CLAIMER_ROLE` from becoming a referrer since then they couldn't collect fees associated with their address.

**Cyfrin:** Verified. We note that `AccessControl::grantRole` has not been overridden such that a referrer could be granted `CLAIMER_ROLE` which would prevent them from claiming referrals associated with their address.
