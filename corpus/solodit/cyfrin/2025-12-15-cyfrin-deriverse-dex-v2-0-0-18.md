---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-0-18
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Using the underlying price instead of the perp price can cause problems
vuln_class: []
---

# Using the underlying price instead of the perp price can cause problems

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** Currently, we use the perp price only for buy/sell operations and for funding rate calculations. However, when calculating the perp value we rely on the underlying price:

Scenerio with perp withdrawal:
The mark price is 100k, and the index price is also 100k.
A user buys a 1 BTC perpetual contract at 100k with 10× leverage. The notional position is 1 BTC, and the user’s account balance becomes –90k.
Later, the index price increases to 120k, while the mark price remains unchanged.
At this point, the user is able to withdraw 18k, bringing their account balance to –108k.
However, the actual perp price is still 100k for 1 BTC. However, the user’s funds are –108k, and their position can only cover 100k

This issue arises because we are using the underlying price to calculate the perp value.

**Impact:** The impact is high, as it allows users to withdraw more funds than they should based on the actual perp price.

**Recommended Mitigation:** Consider using the perp price instead of the underlying price to mitigate this issue.

**Deriverse:** Fixed in commit [1ef948](https://github.com/deriverse/protocol-v1/commit/1ef948af18b47f3e502d0054d760212d4b6263f1).

**Cyfrin:** Verified.
