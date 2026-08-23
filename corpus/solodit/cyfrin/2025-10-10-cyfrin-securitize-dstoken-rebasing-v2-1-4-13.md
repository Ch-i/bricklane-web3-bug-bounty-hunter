---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-4-13
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: Return fast in `ComplianceServiceRegulated::checkHoldUp` if platform wallet
vuln_class: []
---

# Return fast in `ComplianceServiceRegulated::checkHoldUp` if platform wallet

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** `ComplianceServiceRegulated::checkHoldUp` should return fast if `_isPlatformWalletFrom == true`; there's no reason to do all the processing in that case:
```solidity
    function checkHoldUp(
        address[] memory _services,
        address _from,
        uint256 _value,
        bool _isUSLockPeriod,
        bool _isPlatformWalletFrom
    ) internal view returns (bool hasHoldUp) {
        // platform wallets have no lock period so return false (default)
        // and skip all processing if it is a platform wallet
        if(!_isPlatformWalletFrom) {
            ComplianceServiceRegulated complianceService
                = ComplianceServiceRegulated(_services[COMPLIANCE_SERVICE]);
            uint256 lockPeriod;
            if (_isUSLockPeriod) {
                lockPeriod = IDSComplianceConfigurationService(_services[COMPLIANCE_CONFIGURATION_SERVICE]).getUSLockPeriod();
            } else {
                lockPeriod = IDSComplianceConfigurationService(_services[COMPLIANCE_CONFIGURATION_SERVICE]).getNonUSLockPeriod();
            }

            hasHoldUp =
                complianceService.getComplianceTransferableTokens(
                    _from, block.timestamp, uint64(lockPeriod)) < _value;
        }
    }
```

**Securitize:** Fixed in commit [c407d0c](https://github.com/securitize-io/dstoken/commit/c407d0c5a7d702629db5a1fed1b65347078cea9d).

**Cyfrin:** Verified.
