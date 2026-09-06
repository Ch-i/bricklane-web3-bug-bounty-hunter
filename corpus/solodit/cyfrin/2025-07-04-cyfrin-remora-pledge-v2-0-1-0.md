---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-1-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: '`PledgeManager::refundTokens` doesn''t decrement `tokensSold` when pledge
  hasn''t concluded, preventing pledge from reaching its funding goal'
vuln_class: []
---

# `PledgeManager::refundTokens` doesn't decrement `tokensSold` when pledge hasn't concluded, preventing pledge from reaching its funding goal

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** `PledgeManager::refundTokens` doesn't decrement `tokensSold` when pledge hasn't concluded.

**Impact:** The pledge will be prevented from reaching its funding goal since the refunded tokens can't be purchased by other users.

**Recommended Mitigation:** `PledgeManager::refundTokens` should always decrement `tokensSold`:
```diff
        if (
            !pledgeRoundConcluded &&
            SafeCast.toUint32(block.timestamp) < deadline
        ) {
            refundAmount -= (refundAmount * earlySellPenalty) / 1e6;
            _propertyToken.adminTransferFrom(
                signer,
                holderWallet,
                numTokens,
                false,
                false
            );
            emit TokensUnPledged(signer, numTokens);
        } else {
            fee = (userPay.fee / userPay.tokensBought) * numTokens;
            _propertyToken.burnFrom(signer, numTokens);
            emit TokensRefunded(signer, numTokens);
-           tokensSold -= numTokens;
        }

+      tokensSold -= numTokens;
```

**Remora:** Fixed in commit [6be4660](https://github.com/remora-projects/remora-smart-contracts/commit/6be4660990ebafbb7200425978f078a0865732fe).

**Cyfrin:** Verified.
