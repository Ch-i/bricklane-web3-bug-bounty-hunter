---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-23-cyfrin-strata-shares-cooldown-v2-0-0-5
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-01-23T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-23-cyfrin-strata-shares-cooldown-v2-0
title: Increase in coverage can lead to a grief attack causing a DoS for previous
  withdrawal requests
vuln_class: []
---

# Increase in coverage can lead to a grief attack causing a DoS for previous withdrawal requests

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md)_

---

**Description:** This issue demonstrates how an increment in the `coverage`, caused by **a) a large withdrawal on the SR Tranche**, or **b) an increment on the JR deposits**, can be leveraged to pull off a DoS attack on demand and affect both instant and normal (once the cooldown period is over) finalizations.

The fix for issue [*Finalizing withdrawal requests on the `SharesCooldown` contract allows for third-parties to override user’s chosen output token*](#finalizing-withdrawal-requests-on-the-sharescooldown-contract-allows-for-thirdparties-to-override-users-chosen-output-token) addresses an issue with the permissionless`finalize` function. However, even with that fix, this issue can still be pulled off for withdrawals requesting `USDe`, and the fix for issue [*`SharesCooldown` instant finalization can be DoSed because of the `UnstakeCooldown` request limits*](#sharescooldown-instant-finalization-can-be-dosed-because-of-the-unstakecooldown-request-limits) only addresses the problem on instant finalizations.

Following the premise behind the cooldown period and fees based on the current `coverage`.
- High coverage => Low cooldown and fees
- Low coverage => High cooldown and fees

Attackers can grief legitimate users' withdrawals from the SR Tranche requesting `USDe` in a scenario where, after the withdrawal, `coverage` goes from a lower range (more restrictive) to a higher range (less restrictive), withdrawal conditions improves, which means that subsequent withdrawals will take less cooldown time + the attacker knows the end time of the real withdrawal's shares cooldown.

An example of an attack derived from an increment in coverage would look like this:
1. A withdrawal requesting `USDe` from the SR Tranche.
2. `coverage` increments and goes to a less restrictive range. Coverage is incremented either by a) the withdrawal on step 1 (a large withdrawal), or b) an increment on the deposits on the JR Tranche.
3. An attacker requests small withdrawals, asking for `USDe` as the asset to receive, setting the withdrawer of step 1 as the `receiver`.
- All these withdrawals will have a lower cooldown because the `coverage` is on a better range than the range at which the withdrawal from step 1 was processed.
4. Time passes, and as these withdrawals' cooldown is over, the attacker finalizes them, lowering the number of `activeRequests` for the withdrawer on the `SharesCooldown` and incrementing the queue for the withdrawer on the `UnstakeCooldown.
5. As the number of `activeRequests` on the `SharesCooldown` decrements, while the first withdrawal request is under cooldown, the attacker can continue to repeat steps 3-5 to drive the queue of the withdrawer on the `UnstakeCooldown` to its limit, and have more withdrawal requests cooling down on the `SharesCooldown`.
6. Once the first withdrawal passes the cooldown period, the withdrawer attempts to finalize it, but because the `UnstakeCooldown`'s queue for the withdrawer is complete, the finalization attempt reverts with error `ExternalReceiverRequestLimitReached`.

**Impact:** SR withdrawals can be temporarily DoSed when they request to withdraw `USDe`

**Recommended Mitigation:** Given that issue [*`SharesCooldown` instant finalization can be DoSed because of the `UnstakeCooldown` request limits*](#sharescooldown-instant-finalization-can-be-dosed-because-of-the-unstakecooldown-request-limits) by itself only prevents the DoS on the instant finalizations. The recommended mitigation for issue [*Finalizing withdrawal requests on the `SharesCooldown` contract allows for third-parties to override user’s chosen output token*](#finalizing-withdrawal-requests-on-the-sharescooldown-contract-allows-for-thirdparties-to-override-users-chosen-output-token) would not address this issue for the normal finalizations, the suggested mitigation to fully cover all the DoS scenarios accounting for the fixes of both problems (#15 and [*Finalizing withdrawal requests on the `SharesCooldown` contract allows for third-parties to override user’s chosen output token*](#finalizing-withdrawal-requests-on-the-sharescooldown-contract-allows-for-thirdparties-to-override-users-chosen-output-token)), the fix for this issue would be:
- **Create a new `finalize` function that is permissioned and only allows the withdrawer to call it.** The difference between this function and the suggested mitigation for [*Finalizing withdrawal requests on the `SharesCooldown` contract allows for third-parties to override user’s chosen output token*](#finalizing-withdrawal-requests-on-the-sharescooldown-contract-allows-for-thirdparties-to-override-users-chosen-output-token) is that **this new function should allow the withdrawer to specify the asset to receive**, whilst the permissionless version should not (The permissionless version must preserve the original choice at the moment of the withdrawal request).

**Strata:** Fixed in commit [0354983](https://github.com/Strata-Money/contracts-tranches/commit/03549831cf5912b15d9a0eac2bdcfae7e1c395d8).

**Cyfrin:** Verified. New function `SharesCooldown::finalizeWithTokenOverride` allows the withdrawers to finalize their withdrawal requests, specifying the `token` they wish to receive

\clearpage
