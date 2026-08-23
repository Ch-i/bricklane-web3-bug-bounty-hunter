---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-16-cyfrin-accountable-v2-0-4-4
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-10-16T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-16-cyfrin-accountable-v2-0
title: Incorrect event emission is possible in `AccountableAsyncRedeemVault::cancelRedeemRequest`
  flows
vuln_class: []
---

# Incorrect event emission is possible in `AccountableAsyncRedeemVault::cancelRedeemRequest` flows

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-16-cyfrin-accountable-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md)_

---

**Description:** `cancelRedeemRequest()` takes "requestID" as input, but it is never used and never validated to be associated with the input controller address.

All cancellation flows (immediate/ async) work with the requestID of the controller address stored in `_requestIds[controller]`, but the input requestID is only used for event data in `CancelRedeemRequest()` and `CancelRedeemClaimable()` events.

Because this is never verified, caller can input any requestID and have it emitted in the events.

**Impact:** Incorrect event emission is possible, potentially leading to data corruption for the frontend and anyone else using this event data.

**Recommended Mitigation:** Remove the "requestID" parameter from the `cancelRedeemRequest()` function definition and simply use the existing requestID of the controller in event emission.

**Accountable:** Fixed in commits [`aa64491`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/aa64491b1ebe68375793efbc961a323ea739f58c) and [`0675c3d`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/0675c3de2f4eae3456470f04a2241c8f60255088).

**Cyfrin:** Verified. The redeem request of the controller is now used.
