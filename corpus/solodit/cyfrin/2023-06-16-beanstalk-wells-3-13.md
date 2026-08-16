---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-06-16-beanstalk-wells-3-13
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-06-16T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-16-Beanstalk%20wells.md
tags:
- firm:cyfrin
- report:2023-06-16-beanstalk-wells
title: Use constant variables in place of inline magic numbers
vuln_class: []
---

# Use constant variables in place of inline magic numbers

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-06-16-Beanstalk wells.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-16-Beanstalk%20wells.md)_

---

When using numbers, it should be made clear what the number represents by storing it as a constant variable.

For example, in `Well.sol`, the calldata location of the pumps is given by the following:

```solidity
uint dataLoc = LOC_VARIABLE + numberOfTokens() * 32 + wellFunctionDataLength();
```

Without additional knowledge, it may be difficult to read and so it is recommended to assign variables such as:

```solidity
uint256 constant ONE_WORD = 32;
uint256 constant PACKED_ADDRESS = 20;
...
uint dataLoc = LOC_VARIABLE + numberOfTokens() * ONE_WORD + wellFunctionDataLength();
```

The same recommendation can be applied to inline assembly blocks, which perform shifts such that numbers like `248` and `208` have some verbose meaning.

Additionally, when packing values in immutable data/storage, the code would benefit from a note explicitly stating where this is the case, e.g. pumps.

**Beanstalk:** Converted instances of `32` and `20` to `ONE_WORD` and `PACKED_ADDRESS`. Fixed [here](https://github.com/BeanstalkFarms/Basin/pull/66).

**Cyfrin:** Acknowledged.
