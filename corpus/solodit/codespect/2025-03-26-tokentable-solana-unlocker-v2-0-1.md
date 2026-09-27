---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-03-26-tokentable-solana-unlocker-v2-0-1
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-03-26T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-03-26-TokenTable-Solana-Unlocker-V2.md
tags:
- firm:codespect
- report:2025-03-26-tokentable-solana-unlocker-v2
title: '[M-02] Collision between PendingAmountClaimableForCancelledActualsAccount
  may lead to stolen funds'
vuln_class: []
---

# [M-02] Collision between PendingAmountClaimableForCancelledActualsAccount may lead to stolen funds

_Section severity (from Solodit section header): Medium_  
_Audit firm: CODESPECT_  
_Source report: [2025-03-26-TokenTable-Solana-Unlocker-V2.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-03-26-TokenTable-Solana-Unlocker-V2.md)_

---

**Files:** [`claim.rs`](https://github.com/EthSign/tokentable-unlocker-solana/blob/7516b8c86cb305f9d9eb3ac77e7fcd7c6b60cc2f/programs/unlocker-v2-solana/src/instructions/claim.rs)

**Description:**

The `PendingAmountClaimableForCancelledActualsAccount` account is used to store amount assets that a recipient of a cancelled Actual can still claim. This account is provided to the `claim` instruction, and a recipient should be able to claim it.

The problem is that the account seeds don’t contain the `preset_id` where the claim was present. Hence the following scenario is possible:

1. Unlocker is created with two Presets;
2. For each Preset one Actual is created: Actual-1 and Actual-2, for recipient-1 and recipient-2. As those Actuals are created for different Presets, they share the same `actual_id` (e.g. 1);
3. Unlocker’s owner cancels Actual-1 and hence `PendingAmountClaimableForCancelledActualsAccount` is created using `actual_id` 1 as its seed;
4. The recipient-2 can call `claim`, and provide the above `PendingAmountClaimableForCancelledActualsAccount` account to claim the amount stored there, which does not belong to him;

**Impact:** Cancelled amounts can be claimed by other recipients.

**Recommendation:** Add the `preset_id` to the `PendingAmountClaimableForCancelledActualsAccount` seed.

**Status:** Fixed

**Update from TokenTable:** Added `preset_id` to the list of seeds used when deriving `PendingAmountClaimableForCancelledActualsAccount` in [3510bac21534d846d7f117ac89b11d83478a529f](https://github.com/EthSign/tokentable-unlocker-solana/tree/3510bac21534d846d7f117ac89b11d83478a529f).
