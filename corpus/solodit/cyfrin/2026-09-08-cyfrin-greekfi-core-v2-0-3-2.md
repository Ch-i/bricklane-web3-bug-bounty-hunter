---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-08-cyfrin-greekfi-core-v2-0-3-2
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-09-08T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-08-cyfrin-greekfi-core-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-08-cyfrin-greekfi-core-v2-0
title: '`Receipt::collectFees` reads `factory.owner()` twice'
vuln_class: []
---

# `Receipt::collectFees` reads `factory.owner()` twice

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-08-cyfrin-greekfi-core-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-08-cyfrin-greekfi-core-v2.0.md)_

---

**Description:** `Receipt::collectFees` makes two external calls to `factory.owner()`, once as the transfer recipient and once for the `Fee` event:

```solidity
function collectFees(address token) external nonReentrant {
    if (feeAccrued[token] == 0) return; // virgin slot (leg never accrued) — guards the c - 1 below
    uint256 c = feeAccrued[token] - 1; // strip the 1-wei floor → the real collectible
    if (c == 0) return; // only the floor remained; nothing to collect
    feeAccrued[token] = 1;
    IERC20(token).safeTransfer(factory.owner(), c);
    emit Fee(token, factory.owner(), c);
}
```

One call and a local suffices, and it also guarantees the event names the address that received the tokens.

**Recommended Mitigation:**
```solidity
address to = factory.owner();
IERC20(token).safeTransfer(to, c);
emit Fee(token, to, c);
```

**GreekFi:** Fixed in [PR37](https://github.com/greekfi/contracts/pull/37)

**Cyfrin:** Verified. Receipt now reads the Factory owner once and reuses that address for both the transfer and event.

\clearpage
