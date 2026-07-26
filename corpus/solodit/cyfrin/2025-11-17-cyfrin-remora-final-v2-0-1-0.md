---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-17-cyfrin-remora-final-v2-0-1-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-11-17T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-17-cyfrin-remora-final-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-17-cyfrin-remora-final-v2-0
title: Users can reset the status of their `firstPurchase` on the `referralData` when
  the `stablecoin` doesn't revert on transfers to `address(0)`
vuln_class: []
---

# Users can reset the status of their `firstPurchase` on the `referralData` when the `stablecoin` doesn't revert on transfers to `address(0)`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-17-cyfrin-remora-final-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-17-cyfrin-remora-final-v2.0.md)_

---

**Description:** Users can create a referral to get a discount by calling [`ReferralManager::createReferral`](https://github.com/remora-projects/remora-dynamic-tokens/blob/final-audit-prep/contracts/CoreContracts/ReferralManager/ReferralManager.sol#L129-L145). The user receives a discount, and the referrer gets a bonus when the user makes their first purchase.

The system intends to give users a discount only once, but there is an edge case when the stablecoin allows transfer to address(0). This allows calling `ReferralManager::createReferral` and setting the `referrer` as `address(0)`. This effectively bypasses the check to validate if the user has already set a referrer and proceeds to set their `referralData.isFirstPurchase` as true, granting the discount to the user on the next purchase. This allows users to:
1. Call `ReferralManager::createReferral` setting `referrer` as address(0)
2. Purchase a token
3. Call `ReferralManager::createReferral` again setting `referrer` as address(0)

**Impact:** Users can game the referral system to receive a discount on all their purchases by resetting the `firstPurchase` status to true.

**Recommended Mitigation:** When creating the referral, validate that the `referrer` address is not the address(0).
Alternatively, acknowledge this issue and make sure the signers never generate a signature for the `referrer` set as address(0).

**Remora:** Fixed in commit [20eddec](https://github.com/remora-projects/remora-dynamic-tokens/commit/20eddec6e760c7c9bd3669c250e50e562312dfff)

**Cyfrin:** Verified.

\clearpage
