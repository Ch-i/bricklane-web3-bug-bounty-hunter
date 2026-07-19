---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-1-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: '`TokenBank::withdrawFunds` resets `memory` not `storage` fee and sale amounts
  allowing multiple withdraws for the same token'
vuln_class: []
---

# `TokenBank::withdrawFunds` resets `memory` not `storage` fee and sale amounts allowing multiple withdraws for the same token

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** `TokenBank::withdrawFunds` resets `memory` not `storage` fee and sale amounts allowing multiple withdraws for the same token:
```solidity
    function withdrawFunds(
        address tokenAddress,
        bool fee
    ) public nonReentrant restricted {
        TokenData memory curData = tokenData[tokenAddress];
        address to;
        uint64 amount;
        if (fee) {
            to = custodialWallet;
            amount = curData.feeAmount;
            curData.feeAmount = 0; // @audit resets memory not storage
        } else {
            to = curData.withdrawTo;
            amount = curData.saleAmount;
            curData.saleAmount = 0; // @audit resets memory not storage
        }
        if (amount != 0) IERC20(stablecoin).transfer(to, amount);

        if (fee) emit FeesClaimed(tokenAddress, amount);
        else emit FundsClaimed(tokenAddress, amount);
    }
```

**Impact:** The admin can make multiple fee and sale amount withdraws for the same token address. This will work as long as there are sufficient fee and sale tokens from other sales.

**Recommended Mitigation:** Reset `storage` not `memory`:
```diff
    function withdrawFunds(
        address tokenAddress,
        bool fee
    ) public nonReentrant restricted {
        TokenData memory curData = tokenData[tokenAddress];
        address to;
        uint64 amount;
        if (fee) {
            to = custodialWallet;
            amount = curData.feeAmount;
-           curData.feeAmount = 0;
+           tokenData[tokenAddress].feeAmount = 0;
        } else {
            to = curData.withdrawTo;
            amount = curData.saleAmount;
-           curData.saleAmount = 0;
+           tokenData[tokenAddress].saleAmount = 0;
        }
        if (amount != 0) IERC20(stablecoin).transfer(to, amount);

        if (fee) emit FeesClaimed(tokenAddress, amount);
        else emit FundsClaimed(tokenAddress, amount);
    }
```

**Remora:** Fixed in commit [571bfe4](https://github.com/remora-projects/remora-smart-contracts/commit/571bfe4b3129d1acaee62e323a3165c7b1c0f3d1).

**Cyfrin:** Verified.
