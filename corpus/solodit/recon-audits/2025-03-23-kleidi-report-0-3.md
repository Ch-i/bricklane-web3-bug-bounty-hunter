---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-kleidi-report-0-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Kleidi_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-kleidi-report
title: '[L-04] `Timelock` encoding of bytes is unambigous while strings may cause
  issues'
vuln_class: []
---

# [L-04] `Timelock` encoding of bytes is unambigous while strings may cause issues

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Kleidi_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Kleidi_Report.md)_

---

**Encoding (UI risk)** 

This test fails

```solidity
    bytes wrongCheck = "a54D3c09E34aC96807c1CC397404bF2B98DC4eFb";
    bytes rightCheck = "a54d3c09E34aC96807c1CC397404bF2B98DC4eFb";

    function test_bytes_checksum() public {
        bytes32 kak1 = keccak256(wrongCheck);
        bytes32 kak2 = keccak256(rightCheck);

        assertEq(kak1, kak2, "same res");
    }
```

This doesn't
```solidity
    bytes wrongCheck = hex"a54D3c09E34aC96807c1CC397404bF2B98DC4eFb";
    bytes rightCheck = hex"a54d3c09E34aC96807c1CC397404bF2B98DC4eFb";

    function test_bytes_checksum() public {
        bytes32 kak1 = keccak256(wrongCheck);
        bytes32 kak2 = keccak256(rightCheck);

        assertEq(kak1, kak2, "same res");
    }
```

Because the first one is converting the bytes to literals
While the second one is converting them from hex, which is consistent with encodePacked values

It's important that while the UI shows user friendly values, that all values passed to the smart contract are `hex` bytes, to avoid additional layers of encoding
