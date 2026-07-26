---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-10-cyfrin-casimir-v2-0-0-3
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-07-10T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md
tags:
- firm:cyfrin
- report:2024-07-10-cyfrin-casimir-v2-0
title: Anyone can submit proofs via  EigenPod `verifyAndProcessWithdrawals` to break
  the accounting of `withdrawRewards`
vuln_class: []
---

# Anyone can submit proofs via  EigenPod `verifyAndProcessWithdrawals` to break the accounting of `withdrawRewards`

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-10-cyfrin-casimir-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md)_

---

**Description:** `CasimirManager::withdrawRewards` is an `onlyReporter` operation that performs the key tasks below:

1. Submits proofs related to the partial withdrawal of a validator at a given index.
2. Updates the `delayedRewards` based on the last element in the array of `userDelayedWithdrawalByIndex`.

Note that anyone, not just the pod owner, can submit proofs directly to `EigenPod::verifyAndProcessWithdrawals`. In such a case, the `delayedRewards` will not be updated, and the subsequent accounting during report finalization will be broken.

Any attempt to withdraw rewards by calling `CasimirManager::withdrawRewards` will revert because the withdrawal has already been processed. Consequently, `delayedRewards` will never be updated.

This same issue is applicable when submitting proofs for processing a full withdrawal. Critical accounting parameters that are updated in `CasimirManager::withdrawValidator` are effectively bypassed when proofs are directly submitted to EigenLayer.

**Impact:** If `delayedRewards` is not updated, the `rewardStakeRatioSum` and `latestActiveBalanceAfterFee` accounting will be broken.

**Recommended Mitigation:** EigenLayer does not restrict access to process withdrawals only to the pod owner. To that extent, access control to `CasimirManager::withdrawRewards` can always be bypassed. Assuming that all withdrawals will happen only through a reporter, consider adding logic that directly tracks the `eigenWithdrawals.delayedWithdrawals` and `eigenWithdrawals.delayedWithdrawalsCompleted` on EigenLayer to calculate delayedRewards.

**Casimir:**
Fixed in [eb31b43](https://github.com/casimirlabs/casimir-contracts/commit/eb31b4349e69eb401615e0eca253e9ab8cc0999d)

**Cyfrin:** Verified.
