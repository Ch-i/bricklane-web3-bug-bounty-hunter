---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-3-26
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: '`IBeanstalk` interface should be updated to reference Stem-based deposits'
vuln_class: []
---

# `IBeanstalk` interface should be updated to reference Stem-based deposits

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

The [`IBeanstalk`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/interfaces/IBeanstalk.sol#L26) interface currently references the old interface for a number of functions and should be updated:

```diff
    function transferDeposits(
        address sender,
        address recipient,
        address token,
-        uint32[] calldata seasons,
+        int96[] calldata stems,
        uint256[] calldata amounts
    ) external payable returns (uint256[] memory bdvs);

    ...

    function convert(
        bytes calldata convertData,
-        uint32[] memory crates,
+        int96[] memory stems,
        uint256[] memory amounts
    ) external payable returns (int96 toStem, uint256 fromAmount, uint256 toAmount, uint256 fromBdv, uint256 toBdv);

    function getDeposit(
        address account,
        address token,
-        uint32 season
+        int96 stem
    ) external view returns (uint256, uint256);
```
