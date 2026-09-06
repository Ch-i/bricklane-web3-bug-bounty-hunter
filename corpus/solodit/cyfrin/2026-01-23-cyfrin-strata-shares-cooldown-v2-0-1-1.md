---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-23-cyfrin-strata-shares-cooldown-v2-0-1-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-01-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-23-cyfrin-strata-shares-cooldown-v2-0
title: Allowance-Based Withdrawals Can Revert Due to Cooldown Request Slot Limits
vuln_class: []
---

# Allowance-Based Withdrawals Can Revert Due to Cooldown Request Slot Limits

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md)_

---

**Description:** The tranche withdraw/redeem logic allows third parties to withdraw on behalf of a user via allowance:
```solidity
if (caller != owner) {
    _spendAllowance(owner, caller, sharesGross);
}
```
When such a withdrawal is executed using `SharesLock` exit mode, the shares are transferred into the cooldown system and a redeem request is created via `requestRedeem`.

Inside `requestRedeem`, cooldown requests are rate-limited for external receivers:
```solidity
if (initialFrom != to && requestsCount >= PUBLIC_REQUEST_SLOTS_CAP) {
    revert ExternalReceiverRequestLimitReached(...);
}
```
This condition treats any case where `initialFrom != to` as an external receiver, including scenarios where a trusted third party withdraws via allowance and sets `to = caller`. As a result, legitimate allowance-based `withdrawals` can unexpectedly hit the public request slot cap and revert.

This behavior is non-obvious and not enforced at the allowance-checking level, creating an implicit constraint on delegated withdrawals that integrators and users are unlikely to anticipate.

**Impact:** Allowance-based withdrawals using SharesLock can unexpectedly revert due to cooldown request slot limits, breaking integrations and delegated workflows.

**Recommended Mitigation:** Explicitly account for allowance-based withdrawals in cooldown request validation, or clearly document this limitation and its implications for delegated withdrawals.

**Strata:** Fixed in commit [6a9d7a7](https://github.com/Strata-Money/contracts-tranches/commit/6a9d7a7ace616a115a62245b463f6abf89d1ca5f).

**Cyfrin:** Verified. Now, when the `receiver` is either the `caller` or the `owner`, `initialFrom` is set as the `receiver`, which treats the withdrawal request as a `Private Request` and does not count toward the `Public Limit Cap`.
