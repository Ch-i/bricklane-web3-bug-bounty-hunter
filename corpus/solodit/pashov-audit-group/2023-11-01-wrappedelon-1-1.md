---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-11-01-wrappedelon-1-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-11-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-11-01-WrappedElon.md
tags:
- firm:pashov-audit-group
- report:2023-11-01-wrappedelon
title: '[L-02] Wrapped token name is the unwrapped token name'
vuln_class: []
---

# [L-02] Wrapped token name is the unwrapped token name

_Section severity (from Solodit section header): Low_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-11-01-WrappedElon.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-11-01-WrappedElon.md)_

---

The `WrappedElon` contract serves as a wrapper for `$ELON` tokens. Here is how its constructor looks like:

```solidity
constructor() ERC20("Dogelon", "ELON") {}
```

The problem is that instead of naming the token with the same name, prepended with the "Wrapped" word, it is using the same name as the unwrapped version. This can lead to confusions, especially if a liquidity pool is created with the wrapped token for some reason. Change the constructor in the following way:

```diff
-constructor() ERC20("Dogelon", "ELON") {}
+constructor() ERC20("WrappedDogelon", "WELON") {}
```
