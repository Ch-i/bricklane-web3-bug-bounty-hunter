---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-20-cyfrin-aarc-btcy-v2-0-2-7
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-02-20T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-20-cyfrin-aarc-btcy-v2-0
title: '`IBTCYHub::_processSubscription` should follow Checks-Effects-Interactions
  pattern by updating depositor amount before making external call to mint tokens'
vuln_class: []
---

# `IBTCYHub::_processSubscription` should follow Checks-Effects-Interactions pattern by updating depositor amount before making external call to mint tokens

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-20-cyfrin-aarc-btcy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md)_

---

**Description:** `IBTCYHub::_processSubscription` should follow the Checks-Effects-Interactions pattern by updating depositor amount before making an external call to mint tokens:
```diff
-       // Mint tokens to captured user
-       $.ibtcy.mint(user, ibtcyOwed);

        // Update depositor amount
        unchecked {
            uint256 remainingDepositAmount = depositorAmount - processedAmount;
            if (remainingDepositAmount != 0) {
                depositor.amountDepositedMinusFees = remainingDepositAmount;
            } else {
                delete $.depositIdToDepositor[depositId];
            }
        }

+       // Mint tokens to captured user
+       $.ibtcy.mint(user, ibtcyOwed);
```

**Aarc:** Fixed in commit [0b4b41e](https://github.com/aarc-xyz/btcy-contracts-main/commit/0b4b41e12a6c72dd5783eb3adb873383d72d5fe7).

**Cyfrin:** Verified.
