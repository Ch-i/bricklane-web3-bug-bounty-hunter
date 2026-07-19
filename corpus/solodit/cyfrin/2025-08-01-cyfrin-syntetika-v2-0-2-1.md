---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-01-cyfrin-syntetika-v2-0-2-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-08-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-01-cyfrin-syntetika-v2-0
title: Non-compliant users can claim withdrawn assets after the cooldown period
vuln_class: []
---

# Non-compliant users can claim withdrawn assets after the cooldown period

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-01-cyfrin-syntetika-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md)_

---

**Description:** `StakingVault::redeem, withdraw` use the `onlyWhitelisted` modifier to verify that `msg.sender` is whitelisted or is compliant, as this modifier ends up calling `Whitelist::isAddressWhitelisted`:
```solidity
function isAddressWhitelisted(address user) public view returns (bool) {
    if (manualWhitelist[user] || globalWhitelist) {
        return true;
    }

    return complianceChecker.isCompliant(user);
}
```

If a user was whitelisted or was compliant when they created the withdrawal/redemption, but was then removed from the whitelist or became non-compliant, they will still be able to call `StakingVault::claimWithdraw` to withdraw their assets after the cooldown period.

**Recommended Mitigation:** `StakingVault::claimWithdraw` should use modifier `onlyWhitelisted(msg.sender)` to ensure that the caller is still whitelisted or compliant; `onlyWhitelisted(receiver)` could also be used to enforce that the destination address is also whitelisted.

**Syntetika:**
Fixed in commit [86384fe](https://github.com/SyntetikaLabs/monorepo/commit/86384fe1504780338649d25f720fb78b25132875) by removing the whitelist functionality entirely from `StakingVault` to resolve finding L-4.

**Cyfrin:** Verified.
