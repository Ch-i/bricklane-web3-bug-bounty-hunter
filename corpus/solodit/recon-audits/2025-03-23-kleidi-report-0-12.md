---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-kleidi-report-0-12
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Kleidi_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-kleidi-report
title: '[L-13] `InstanceDeployer` - Could use constant for Flag Previous Owner'
vuln_class: []
---

# [L-13] `InstanceDeployer` - Could use constant for Flag Previous Owner

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Kleidi_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Kleidi_Report.md)_

---

Could use CONSTANT instead of `1`

https://github.com/solidity-labs-io/kleidi/blob/1a06ac16bc99d0b4081281329d03064c3737f5e4/src/InstanceDeployer.sol#L294-L302

```solidity
            calls3[index++].callData = abi.encodeWithSelector(
                OwnerManager.swapOwner.selector,
                /// previous owner
                address(1),
                /// old owner (this address)
                address(this),
                /// new owner, the first owner the caller wants to add
                instance.owners[0]
            );
```
