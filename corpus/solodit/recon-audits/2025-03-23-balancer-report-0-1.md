---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-balancer-report-0-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Balancer_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-balancer-report
title: '[L-02] Operative Gotcha - Safe.getModules is limited to the first 10 modules'
vuln_class: []
---

# [L-02] Operative Gotcha - Safe.getModules is limited to the first 10 modules

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Balancer_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Balancer_Report.md)_

---

**Impact**

`_isModuleEnabled` is written as follows:

https://github.com/onchainification/aura_locker_v2/blob/07294ae3638909ecd768a6a0f831fa513abe91a0/src/AuraLockerModule.sol#L123

```solidity
    /// @dev The Gnosis Safe v1.1.1 does not yet have the `isModuleEnabled` method, so we need a workaround
    function _isModuleEnabled() internal view returns (bool) {
        address[] memory modules = SAFE.getModules();
        for (uint256 i = 0; i < modules.length; i++) {
            if (modules[i] == address(this)) return true;
        }
        return false;
    }
```

Which uses `getModules`, which is paginated and limited to the first 10 enabled modules

https://etherscan.io/address/0x34cfac646f301356faa8b21e94227e3583fe3f5f#code
```solidity
    function getModules()
        public
        view
        returns (address[] memory)
    {
        (address[] memory array,) = getModulesPaginated(SENTINEL_MODULES, 10);
        return array;
    }
```

It's worth noting that if this module where to be used with a lot of other modules setup, the check could fail

However, current there are no other modules set, meaning that the code is safe as is

Additionally, even if the check were to fail, no particular damage would be caused to the Safe, at worst the `checkUpkeep` would always return false, making no upkeep run, but causing no DOS to the Safe

**Mitigation**

Add a comment to the module and make sure to have less than 10 modules

---
