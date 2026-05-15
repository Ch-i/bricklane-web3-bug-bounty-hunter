---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-11-cyfrin-benqi-ignite-v2-0-1-4
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-12-11T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-11-cyfrin-benqi-ignite-v2-0
title: Ignite fee is not returned for pre-validated `QI` stakes in the event of registration
  failure
vuln_class: []
---

# Ignite fee is not returned for pre-validated `QI` stakes in the event of registration failure

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-11-cyfrin-benqi-ignite-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md)_

---

**Description:** The `1 AVAX` [Ignite fee](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L387) applied to pre-validated `QI` stakes is [paid to the fee recipient](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L388) at the time of registration. If this registration fails (e.g. due to off-chain BLS proof validation), the registration will be [marked as withdrawable](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L620) once `Ignite::releaseLockedTokens` is called; however, since the fee has already been paid and [deducted from the user's stake amount](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L397), it will not be returned with the refunded `QI` stake. This behavior differs from the other registration methods, which all refund the usually non-refundable fee in the event of registration failure.

**Impact:** Users who register with a hosted Zeeve validator will not be refunded the Ignite fee if registration fails.

**Recommended Mitigation:** Refund the Ignite fee if registration fails for pre-validated `QI` stakes.

**BENQI:** Fixed in commit [f671224](https://github.com/Benqi-fi/ignite-contracts/commit/f67122426c5dff6023da1ec9602c1959703db28e).

**Cyfrin:** Verified. The fee is now taken from successful registrations during the call to `Ignite::releaseLockedTokens`.

\clearpage
