---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-3-24
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: Feature flags are not being used in the `TokenLibrary`
vuln_class: []
---

# Feature flags are not being used in the `TokenLibrary`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** `TokenLibrary::setFeature` implements a feature flag system that is completely non-functional in the current codebase. While the infrastructure exists to enable/disable features, no business logic actually checks these feature flags; consider removing this code if it is deprecated or obsolete.

```solidity
 function setFeature(SupportedFeatures storage supportedFeatures, uint8 featureIndex, bool enable) public {
        uint256 base = 2;
        uint256 mask = base**featureIndex;

        // Enable only if the feature is turned off and disable only if the feature is turned on
        if (enable && (supportedFeatures.value & mask == 0)) {
            supportedFeatures.value = supportedFeatures.value ^ mask;
        } else if (!enable && (supportedFeatures.value & mask >= 1)) {
            supportedFeatures.value = supportedFeatures.value ^ mask;
        }
    }
```

**Securitize:** Acknowledged.

\clearpage
