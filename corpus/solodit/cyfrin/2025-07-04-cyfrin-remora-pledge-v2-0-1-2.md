---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-1-2
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
title: Fee should be calculated after first purchase discount is applied in `TokenBank::buy`
  to prevent over-charging users
vuln_class: []
---

# Fee should be calculated after first purchase discount is applied in `TokenBank::buy` to prevent over-charging users

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** `TokenBank::buy` calculates the total purchase amount as being composed of:
* `stablecoinValue` : value of the tokens
* `feeValue` : fee calculated off `stablecoinValue`
```solidity
        uint64 stablecoinValue = amount * curData.pricePerToken;
        uint64 feeValue = (stablecoinValue * curData.saleFee) / 1e6;
```

Afterwards if this is the user's first purchase, they receive a discount on the `stablecoinValue`:
```solidity
        IReferralManager refManager = IReferralManager(referralManager);
        bool firstPurchase = refManager.isFirstPurchase(to);
        if (firstPurchase) stablecoinValue -= refManager.referDiscount();
```

However the fee is not updated so was still calculated from the initial higher `stablecoinValue` amount.

**Impact:** Users will pay higher fees than they should when receiving the first purchase discount.

**Recommended Mitigation:** Only calculate `feeValue` once the discount has been applied:
```diff
        address to = msg.sender;
        uint64 stablecoinValue = amount * curData.pricePerToken;
-       uint64 feeValue = (stablecoinValue * curData.saleFee) / 1e6;

        IReferralManager refManager = IReferralManager(referralManager);
        bool firstPurchase = refManager.isFirstPurchase(to);
        if (firstPurchase) stablecoinValue -= refManager.referDiscount();

+       uint64 feeValue = (stablecoinValue * curData.saleFee) / 1e6;
        curData.saleAmount += stablecoinValue;
        curData.feeAmount += feeValue;
```

**Remora:** Fixed in commits [4aea246](https://github.com/remora-projects/remora-smart-contracts/commit/4aea246c8de4dcd03bc11a5cd87ca617e787bdaf), [5510920](https://github.com/remora-projects/remora-smart-contracts/commit/55109201b0b592abb94a3c73a5f45c9c24b3d440) - changed the way fee calculation works for regulatory reasons.

**Cyfrin:** Verified.
