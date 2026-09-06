---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-1-31
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Inefficient rebalancing can cause the loss of users
vuln_class: []
---

# Inefficient rebalancing can cause the loss of users

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** We can only call rebalance once every 5 minutes. This is enforced through the `check_rebalancing` function, which allows only 25 rebalancing calls each time it runs. This limitation can create significant issues.

For example, if there are 200,000 open positions and `check_rebalancing` is triggered whenever a user performs a perp-related action, we would need roughly 8,000 user-triggered calls every 5 minutes to rebalance all positions. If the number of user actions is lower, many positions will not be rebalanced in time.

This can result in positions being rebalanced too late, which may lead to improper liquidations(early or late liquidation) and potentially increase socialized losses for other users.

**Impact:** This limitation can lead to positions not being rebalanced until much later if perp-related transactions are very low, which can result in improper liquidations.

**Recommended Mitigation:** Implement a function that can be called to rebalance user positions every 5 minutes.

**Deriverse:** Fixed in commit [7873db](https://github.com/deriverse/protocol-v1/commit/7873db50be8fc7298817e097d0f55bf165ceae04), [76dbbe](https://github.com/deriverse/protocol-v1/commit/76dbbec20fdd2e09fa5722e993da897bf0da2f8b).

**Cyfrin:** Verified.
