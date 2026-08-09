---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-20-cyfrin-aarc-btcy-v2-0-2-16
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-02-20T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-20-cyfrin-aarc-btcy-v2-0
title: Zero amount redemption requests can't be cancelled or processed
vuln_class: []
---

# Zero amount redemption requests can't be cancelled or processed

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-20-cyfrin-aarc-btcy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md)_

---

**Description:** When requesting a subscription or redemption, the input restriction on the amount is that it must be greater or equal to the minimum subscription/redemptions amounts.

However the minimum subscription/redemptions amounts can be configured to zero hence zero amount subscriptions or redemptions can be allowed.

In the case of zero amount subscriptions/redemptions these can't subsequently be cancelled or rescued as `IBTCYHub::cancelRedemption,cancelSubscription,rescueRedemption` revert if the amount retrieved from `storage` if zero.

**Recommended Mitigation:** In `IBTCYHub::initialize, setMinimumDepositAmount, setMinimumRedemptionAmount` enforce that minimum subscription/redemption amounts must be greater than zero.

**Aarc:** Fixed in commit [8d6262e](https://github.com/aarc-xyz/btcy-contracts-main/commit/8d6262ec79a768b1986020c89cdfd3ee554925a6).

**Cyfrin:** Verified.
