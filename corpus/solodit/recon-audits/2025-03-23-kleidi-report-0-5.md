---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-kleidi-report-0-5
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
title: '[L-06] `Timelock`  `isSelfAddressCheck` can be removed'
vuln_class: []
---

# [L-06] `Timelock`  `isSelfAddressCheck` can be removed

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Kleidi_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Kleidi_Report.md)_

---

https://github.com/solidity-labs-io/kleidi/blob/1a06ac16bc99d0b4081281329d03064c3737f5e4/src/Timelock.sol#L1166-L1177

```solidity
            if (isSelfAddressCheck[i]) {
                /// self address check, data must be empty
                require(
                    data[i].length == 0,
                    "CalldataList: Data must be empty for self address check"
                );
                require(
                    endIndex - startIndex == 20,
                    "CalldataList: Self address check must be 20 bytes"
                );
                dataHash = ADDRESS_THIS_HASH;
            } else {
```

The hash is known at time of setup, so there's no advantage in having this code
