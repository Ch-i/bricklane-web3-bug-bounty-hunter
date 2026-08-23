---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-01-cyfrin-syntetika-v2-0-3-14
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-08-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-01-cyfrin-syntetika-v2-0
title: '`ComplianceChecker::isCompliant` incorrectly returns `true` if compliance
  options have no required soul bound tokens'
vuln_class: []
---

# `ComplianceChecker::isCompliant` incorrectly returns `true` if compliance options have no required soul bound tokens

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-01-cyfrin-syntetika-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md)_

---

**Description:** `ComplianceChecker::isCompliant` contains a logic flaw that allows universal bypass of all compliance requirements. When a compliance option exists with an empty `requiredSBTs` array (length = 0), the inner verification loop never executes, leaving the compliant variable as true by default

```solidity
function isCompliant(address user) public view returns (bool) {
        // The user can be compliant with any option (KYC or KYB)
        uint256 complianceOptionsLength = _complianceOptions.length;
        for (
            uint256 optionIndex;
            optionIndex < complianceOptionsLength;
            optionIndex++
        ) {
            // But the address must have all the required SBTs for that option (e.g. non-sanctioned and age>18)
            bool compliant = true;
            uint256 requiredSBTsLength = _complianceOptions[optionIndex]
                .requiredSBTs
                .length;
            for (uint sbtIndex; sbtIndex < requiredSBTsLength; sbtIndex++) {
                if (
                    !_complianceOptions[optionIndex]
                        .requiredSBTs[sbtIndex]
                        .isVerificationSBTValid(user)
                ) {
                    compliant = false;
                    break;
                }
            }
            if (compliant) {
                return true; <-----
            }
        }
        return false;
    }

```

Malicious users can exploit this  gaining unauthorized access to deposit addresses calling `registerDepositAddress` with different addressees.

**Impact:** Any address can gain access to deposit addresses without verification.

**Recommended Mitigation:** Add validation to prevent empty options in `setComplianceOptions`

**Syntetika:**
Acknowledged; in practice this is a non-issue as compliance options are set by the admin and always have at least one required Soul Bound Token (SBT).

**Cyfrin:**
