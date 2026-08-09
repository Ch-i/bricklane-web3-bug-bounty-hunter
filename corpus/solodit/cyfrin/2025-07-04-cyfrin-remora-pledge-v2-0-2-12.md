---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-2-12
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: '`PledgeManager::pricePerToken` can only support a maximum price of `$4294`'
vuln_class: []
---

# `PledgeManager::pricePerToken` can only support a maximum price of `$4294`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** `PledgeManager::pricePerToken` uses `uint32` and indicates in the comment it represents USD price using 6 decimals of precision:
```solidity
    uint32 public pricePerToken; //in usd (6 decimals)
```

**Impact:** Since the maximum value of `uint32` is 4294967295, with 6 decimals of precision the maximum USD `pricePerToken` is limited to `$4294`.

This may be insufficient because the goal is to tokenize real-estate which can be worth many millions of dollars.

**Recommended Mitigation:** Use a larger size to store `pricePerToken` if supporting a large USD price is required.

**Remora:** Acknowledged; we plan to keep the price low around say $50 per token.

\clearpage
