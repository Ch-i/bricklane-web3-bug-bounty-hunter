---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-2-6
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: '`DividendManager::distributePayout` records a new payout record increasing
  the current payout index for zero `payoutAmount`'
vuln_class: []
---

# `DividendManager::distributePayout` records a new payout record increasing the current payout index for zero `payoutAmount`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** `DividendManager::distributePayout` records a new payout record increasing the current payout index for zero `payoutAmount`.

**Proof of Concept:**
```solidity
function test_distributePayout_ZeroPayout() external {
    // setup one user
    address user = users[0];
    uint256 userRemoraTokens = 1;

    // whitelist user
    remoraTokenProxy.addToWhitelist(user);
    assertTrue(remoraTokenProxy.isWhitelisted(user));

    // mint user their tokens
    remoraTokenProxy.mint(user, userRemoraTokens);
    assertEq(remoraTokenProxy.balanceOf(user), userRemoraTokens);

    // allowlist user
    allowListProxy.allowUser(user, true, true, false);
    assertTrue(allowListProxy.allowed(user));

    // zero payout distribution - should revert here
    remoraTokenProxy.distributePayout(0);
    // didn't revert but increased current payout index
    assertEq(remoraTokenProxy.getCurrentPayoutIndex(), 1);
}
```

**Recommended Mitigation:** `DividendManager::distributePayout` should revert when `payoutAmount == 0`.

**Remora:** Fixed in commit [c2002fb](https://github.com/remora-projects/remora-smart-contracts/commit/c2002fb751c22d6f4009eaa6f3dd651b5b4ca474).

**Cyfrin:** Verified.
