---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-12-cyfrin-bebop-router-v2-0-4-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-06-12T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-12-cyfrin-bebop-router-v2-0
title: '`HookLib::hooksHash` initializes `nonce` to its default value'
vuln_class: []
---

# `HookLib::hooksHash` initializes `nonce` to its default value

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-12-cyfrin-bebop-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md)_

---

**Description:** `nonce` is explicitly initialized to `0`, which is already its default value in Solidity. The explicit `= 0` assignment is redundant and wastes a small amount of gas.

```
contracts/libraries/HookLib.sol
85:            uint256 nonce = 0;
```

**Recommended Mitigation:**
```solidity
uint256 nonce;
```

**Bebop:** Fixed in commit [9db95bc](https://github.com/bebop-dex/bebop-rfqa/commit/9db95bc2b423d9317c149e90a70ae51565e26367).

**Cyfrin:**
Verified.


\clearpage
