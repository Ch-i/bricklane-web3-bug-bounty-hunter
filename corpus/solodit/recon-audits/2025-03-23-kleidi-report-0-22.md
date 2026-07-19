---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-kleidi-report-0-22
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Kleidi_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-kleidi-report
title: '[L-23] `getFunctionSignature` can be refactored to not use assembly'
vuln_class: []
---

# [L-23] `getFunctionSignature` can be refactored to not use assembly

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Kleidi_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Kleidi_Report.md)_

---

**Impact**

`getFunctionSignature` uses assembly as follows

https://github.com/solidity-labs-io/kleidi/blob/1a06ac16bc99d0b4081281329d03064c3737f5e4/src/BytesHelper.sol#L7-L18

```solidity
    function getFunctionSignature(bytes memory toSlice)
        public
        pure
        returns (bytes4 functionSignature)
    {
        require(toSlice.length >= 4, "No function signature");

        assembly ("memory-safe") {
            functionSignature := mload(add(toSlice, 0x20))
        }
        return bytes4(toSlice);
    }
```

But you can simply cast bytes to bytes4 instead


**Proof Of Concept**

```solidity
    function getFunctionSignature(bytes memory toSlice)
        public
        pure
        returns (bytes4 functionSignature)
    {
        require(toSlice.length >= 4, "No function signature");

        assembly ("memory-safe") {
            functionSignature := mload(add(toSlice, 0x20))
        }
    }

    function test_check(bytes memory theBytes) public {
        vm.assume(theBytes.length >= 4);
        bytes4 res = getFunctionSignature(theBytes);
        bytes4 normal = bytes4(theBytes);

        assertEq(res, normal);
    }
```
