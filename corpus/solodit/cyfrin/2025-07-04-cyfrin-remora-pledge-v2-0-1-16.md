---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-1-16
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: Forwarders who aren't also holders are unable to claim forwarded payouts
vuln_class: []
---

# Forwarders who aren't also holders are unable to claim forwarded payouts

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** Forwarders who aren't also holders are unable to claim forwarded payouts due to this check in `DividendManager::payoutBalance`:
```solidity
    function payoutBalance(address holder) public returns (uint256) {
        HolderManagementStorage storage $ = _getHolderManagementStorage();
        HolderStatus memory rHolderStatus = $._holderStatus[holder];
        uint16 currentPayoutIndex = $._currentPayoutIndex;

        if (
             // @audit must be a holder to claim payouts, prevents forwarders who aren't
             // also holders from claiming their forwarded payouts
            (!rHolderStatus.isHolder) || //non-holder calling the function
            (rHolderStatus.isFrozen && rHolderStatus.frozenIndex == 0) || //user has been frozen from the start, thus no payout
            rHolderStatus.lastPayoutIndexCalculated == currentPayoutIndex // user has already been paid out up to current payout index
        ) return 0;
```

**Impact:** Forwarders who aren't also holders are unable to claim forwarded payouts.

**Recommended Mitigation:** Remove the `(!rHolderStatus.isHolder)` check in `DividendManager::payoutBalance`.

**Remora:** Fixed in commit [82fd5d1](https://github.com/remora-projects/remora-smart-contracts/commit/82fd5d1a7d2c6c54790638d63d748eeb8efc870e).

**Cyfrin:** Verified.

\clearpage
