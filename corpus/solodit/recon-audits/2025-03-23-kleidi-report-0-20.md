---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-kleidi-report-0-20
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Kleidi_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-kleidi-report
title: '[L-21] RecoverySpell Gas Optimizations'
vuln_class: []
---

# [L-21] RecoverySpell Gas Optimizations

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Kleidi_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Kleidi_Report.md)_

---

**Remove address(0) check, this is already done by OZ.ECDSA**

https://github.com/solidity-labs-io/kleidi/blob/1a06ac16bc99d0b4081281329d03064c3737f5e4/src/RecoverySpell.sol#L226-L230

```solidity
            /// will be 0 on the second retrieval and the require will fail.
            require( /// @audit Pretty sure OZ does this
                valid && recoveredAddress != address(0),
                "RecoverySpell: Invalid signature"
            );
```

**Ownership check can be done in memory more cheaply**

The code change is pretty annoying compared to this, but memory should be cheaper

https://github.com/solidity-labs-io/kleidi/blob/1a06ac16bc99d0b4081281329d03064c3737f5e4/src/RecoverySpell.sol#L218-L221

```solidity
            assembly ("memory-safe") {
                valid := tload(recoveredAddress)
                if eq(valid, 1) { tstore(recoveredAddress, 0) } /// @audit Cannot recover more than once per address
            }
```

Copy owners (unnecessary if immutable)
For each of them store `true` in an array at their index

For each signer, find the owner in the array and check that the value was `true`, set the value to `false`

This should cost less because the cost of finding the address will tend to be lower for the average user count (less than 10)
