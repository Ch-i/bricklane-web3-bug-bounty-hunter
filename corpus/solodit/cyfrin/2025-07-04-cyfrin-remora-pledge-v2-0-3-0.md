---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-3-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: Emit missing events for storage changes
vuln_class: []
---

# Emit missing events for storage changes

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** Emit missing events for storage changes:
* `Allowlist::changeUserAccreditation`, `changeAdminStatus`
* `Allowlist::UserAllowed` should be expanded to contain and emit the `HolderInfo` boolean flags
* `ReferralManager::addReferral`
* `RemoraIntermediary::setFundingWallet`, `setFeeRecipient`
* `TokenBank::changeReferralManager`, `changeStablecoin`, `changeCustodialWallet`
* `TokenBank::TokensWithdrawn` should include withdrawn `amount`
* `DividendManager::setPayoutForwardAddress`, `changeWallet`
* `RemoraToken::addToWhitelist`, `removeFromWhitelist`, `updateAllowList`
* `PaymentSettler::withdraw`, `withdrawAllFees` should emit amount withdrawn, `addToken`, `changeCustodian`,  `changeStablecoin`

**Remora:** Fixed in commit [9051af8](https://github.com/remora-projects/remora-smart-contracts/commit/9051af840f92c7aee37b95a4d8f206d0f16abc93).

**Cyfrin:** Verified.
