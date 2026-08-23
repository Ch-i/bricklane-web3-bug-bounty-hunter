---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-04-cyfrin-ethcf-swapboard-v2-0-2-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-03-04T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-ethcf-swapboard-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-04-cyfrin-ethcf-swapboard-v2-0
title: Don't initialize `received` to default value in `Swapboard::createOrder`
vuln_class: []
---

# Don't initialize `received` to default value in `Swapboard::createOrder`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-04-cyfrin-ethcf-swapboard-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-ethcf-swapboard-v2.0.md)_

---

**Description:** Don't initialize `received` to default value in `Swapboard::createOrder`:
```diff
-       uint256 received;
        unchecked {
-           received = balanceAfter - balanceBefore;
+           uint256 received = balanceAfter - balanceBefore;
-       }
        if (received != amountA) {
            revert BalanceMismatch(amountA, received);
        }
+       }
```

**ETHCF:** Fixed in commit [572f3c5](https://github.com/ETHCF/swapboard/commit/572f3c5d724b78fc3a2f304557a23c018f9fc31d).

**Cyfrin:** Verified.
