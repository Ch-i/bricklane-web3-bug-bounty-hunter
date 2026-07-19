---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-4-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: Avoid unnecessary use of `SafeMath` operations
vuln_class: []
---

# Avoid unnecessary use of `SafeMath` operations

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

There are a number of instances as outlined below where the use of `SafeMath` operations can be avoided to save gas due to the fact that these values are already validated or otherwise guaranteed to not overflow:

```solidity
File: /beanstalk/farm/TokenFacet.sol

151:        currentAllowance.sub(subtractedValue)
```

```solidity
File: /beanstalk/market/Listing.sol

194:        l.amount.sub(amount),

220:        l.amount.sub(amount),
```

```solidity
File: /libraries/Token/LibTransfer.sol

69:                token.balanceOf(address(this)).sub(beforeBalance)
```

```solidity
File: /libraries/Silo/LibSilo.sol

264:        s.a[account].roots = s.a[account].roots.sub(roots);
```
