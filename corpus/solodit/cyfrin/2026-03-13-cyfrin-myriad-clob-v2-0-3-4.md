---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-3-4
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-myriad-clob-v2-0
title: Order expiration check uses inclusive bound so order remains valid at the expiration
  timestamp
vuln_class: []
---

# Order expiration check uses inclusive bound so order remains valid at the expiration timestamp

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-myriad-clob-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md)_

---

**Description:** In `MyriadCTFExchange::_validateOrder` we require that an order is not expired before accepting it. The check is `order.expiration == 0 || order.expiration >= block.timestamp`. When `expiration` is non-zero, this treats the order as valid whenever the current time is less than or equal to `expiration`. So at the exact moment `block.timestamp == order.expiration`, the order is still valid.

The field is named `expiration`, which conventionally means the time at which the order expires, i.e. at that instant it should no longer be valid. Allowing validity at the exact expiration timestamp contradicts that meaning and can surprise integrators or users who assume "expiration" is the first moment the order is invalid.

```solidity
// MyriadCTFExchange.sol:409-410
require(order.expiration == 0 || order.expiration >= block.timestamp, "expired");
```

**Recommended Mitigation:** Require that the current time is strictly before the expiration time when `expiration` is set. Change the check to use a strict inequality:

```solidity
require(order.expiration == 0 || order.expiration > block.timestamp, "expired");
```

**Myriad:** Fixed in commit [`0d94334`](https://github.com/Polkamarkets/polkamarkets-js/pull/119/changes/0d9433408a1263abcc4e28f9514e9911a4142cb2)

**Cyfrin:** Verified.
