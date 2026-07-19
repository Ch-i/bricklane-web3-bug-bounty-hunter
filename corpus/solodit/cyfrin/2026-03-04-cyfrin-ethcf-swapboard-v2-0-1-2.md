---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-04-cyfrin-ethcf-swapboard-v2-0-1-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-03-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-ethcf-swapboard-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-04-cyfrin-ethcf-swapboard-v2-0
title: Use read-then-increment in `Swapboard::createOrder, createOrderWithEth`
vuln_class: []
---

# Use read-then-increment in `Swapboard::createOrder, createOrderWithEth`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-04-cyfrin-ethcf-swapboard-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-ethcf-swapboard-v2.0.md)_

---

**Description:** Use read-then-increment in `Swapboard::createOrder, createOrderWithEth`:
```diff
-       orderId = nextOrderId;
-       unchecked {
-           ++nextOrderId;
-       }
+       unchecked { orderId = nextOrderId++; }
```

**ETHCF:** Fixed in commit [572f3c5](https://github.com/ETHCF/swapboard/commit/572f3c5d724b78fc3a2f304557a23c018f9fc31d).

**Cyfrin:** Verified.

\clearpage
