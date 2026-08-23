---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-2-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: Fee refund can lose precision
vuln_class: []
---

# Fee refund can lose precision

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** `PledgeManager::refundTokens` calculates the user fee refund as:
```solidity
fee = (userPay.fee / userPay.tokensBought) * numTokens;
```

**Impact:** The fee refund will be less than it should be due to [division before multiplication](https://dacian.me/precision-loss-errors#heading-division-before-multiplication)

**Recommended Mitigation:** Perform multiplication before division:
```solidity
fee = userPay.fee * numTokens / userPay.tokensBought;
```

**Remora:** Fixed in commit [b69836f](https://github.com/remora-projects/remora-smart-contracts/commit/b69836f4e7effd2f1cc209608b9149671c79bc18).

**Cyfrin:** Verified.
