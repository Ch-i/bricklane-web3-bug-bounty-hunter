---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-20-cyfrin-aarc-btcy-v2-0-2-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-02-20T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-20-cyfrin-aarc-btcy-v2-0
title: Misleading event emission when previous state not changed
vuln_class: []
---

# Misleading event emission when previous state not changed

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-20-cyfrin-aarc-btcy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md)_

---

**Description:** There is an asymmetry in that `AllowList::removeFromAllowlist` doesn't check whether address exists while `batchRemoveFromAllowlist` does.

This means that `removeFromAllowlist` will emit `AddressRemovedFromAllowlist` even though the account was not removed.

**Recommended Mitigation:** `AllowList::removeFromAllowlist` should only emit the `AddressRemovedFromAllowlist` if the account was actually removed similar to `batchRemoveFromAllowlist`.

Similar issue applies to `addToAllowlist` and `batchAddToAllowlist` and potentially to `setAllowlistEnabled`.

In other contracts consider similar behavior in:
* `BTCY::updateTransferDenyList`
* `DepositWithdraw::addTokenToWhitelist, removeTokenFromWhitelist, addUserToWhitelist, removeUserFromWhitelist, batchAddUsersToWhitelist, batchRemoveUsersFromWhitelist, setDepositPaused, setWithdrawalPaused`
* `IBTCYHub::setSubscriptionPaused, setRedemptionPaused`

**Aarc:** Fixed in commit [a94fb04](https://github.com/aarc-xyz/btcy-contracts-main/commit/a94fb042e332716921fdbef2a266ddcd2e038cb8).

**Cyfrin:** Verified.
