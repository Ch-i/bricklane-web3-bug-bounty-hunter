---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-13-cyfrin-zaros-4-9
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-07-13T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md
tags:
- firm:cyfrin
- report:2024-07-13-cyfrin-zaros
title: Needless addition in `TradingAccount::withdrawMarginUsd`
vuln_class: []
---

# Needless addition in `TradingAccount::withdrawMarginUsd`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-13-cyfrin.zaros.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md)_

---

**Description:** Needless addition in `TradingAccount::withdrawMarginUsd` since this is an output variable that has no prior assignment or value:
```solidity
File: TradingAccount.sol
371:             withdrawnMarginUsdX18 = withdrawnMarginUsdX18.add(amountUsdX18);
380:             withdrawnMarginUsdX18 = withdrawnMarginUsdX18.add(marginToWithdrawUsdX18);
```

**Recommended Mitigation:**
```diff
- 371:             withdrawnMarginUsdX18 = withdrawnMarginUsdX18.add(amountUsdX18);
- 380:             withdrawnMarginUsdX18 = withdrawnMarginUsdX18.add(marginToWithdrawUsdX18);

+ 371:             withdrawnMarginUsdX18 = amountUsdX18;
+ 380:             withdrawnMarginUsdX18 = marginToWithdrawUsdX18;
```

**Zaros:** Fixed in commit [672a08b](https://github.com/zaros-labs/zaros-core/commit/672a08b93e288242e6d4088aa1e60a771053982c).

**Cyfrin:** Verified.
