---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-kleidi-report-0-18
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
title: '[L-19] Different Threshold can result in different hash but same config when
  using one owner'
vuln_class: []
---

# [L-19] Different Threshold can result in different hash but same config when using one owner

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Kleidi_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Kleidi_Report.md)_

---

**Impact**

When calling `createSystemInstance`, a Safe with a single owner could be deployed, while passing a threshold that is above 1

Because of the check `if (instance.owners.length > 1) {` the threshold will not be validated in those cases

Because `threshold` is part of the salt, this will result in a unique deployment, which will share the configuration with other deployments


https://github.com/solidity-labs-io/kleidi/blob/1a06ac16bc99d0b4081281329d03064c3737f5e4/src/InstanceDeployer.sol#L308-L329

```solidity
            for (uint256 i = 1; i < instance.owners.length - 1; i++) {
                calls3[index++].callData = abi.encodeWithSelector(
                    OwnerManager.addOwnerWithThreshold.selector,
                    instance.owners[i],
                    1
                );
            }

            /// if there is only one owner, the threshold is set to 1
            /// if there are more than one owner, add the final owner with the
            /// updated threshold
            if (instance.owners.length > 1) {
                /// add final owner with the updated threshold
                /// if threshold is greater than the number of owners, that
                /// will be caught in the addOwnerWithThreshold function with
                /// error "GS201"
                calls3[index++].callData = abi.encodeWithSelector(
                    OwnerManager.addOwnerWithThreshold.selector,
                    instance.owners[instance.owners.length - 1],
                    instance.threshold
                );
            }
```

**Mitigation**

You could enforce that the threshold is met by the number of owners

However there is no particular impact to this finding
