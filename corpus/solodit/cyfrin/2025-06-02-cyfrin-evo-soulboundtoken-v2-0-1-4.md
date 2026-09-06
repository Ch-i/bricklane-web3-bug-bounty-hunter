---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-02-cyfrin-evo-soulboundtoken-v2-0-1-4
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-06-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-02-cyfrin-evo-soulboundtoken-v2.0.md
tags:
- firm:cyfrin
- report:2025-06-02-cyfrin-evo-soulboundtoken-v2-0
title: Consider preventing users from over-paying
vuln_class: []
---

# Consider preventing users from over-paying

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-02-cyfrin-evo-soulboundtoken-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-02-cyfrin-evo-soulboundtoken-v2.0.md)_

---

**Description:** Currently the protocol allows users to over-pay:
```solidity
function _revertIfInsufficientFee() internal view {
    if (msg.value < _getFee()) revert SoulBoundToken__InsufficientFee();
}
```

Consider changing this to require the exact fee to prevent users from accidentally over-paying:
```solidity
function _revertIfIncorrectFee() internal view {
    if (msg.value != _getFee()) revert SoulBoundToken__IncorrectFee();
}
```

[Fat Finger](https://en.wikipedia.org/wiki/Fat-finger_error) errors have previously resulted in notorious unintended errors in financial markets; the protocol could choose to be defensive and help protect users from themselves.

**Evo:**
Fixed in commit [e3b2f74](https://github.com/contractlevel/sbt/commit/e3b2f74239601b2721118e11aaa92b42dbb502e9).

**Cyfrin:** Verified.
