---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-3-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-07-07T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-07-cyfrin-suzaku-core-v2-0
title: Wrong revert reason In `onSlash` functionality
vuln_class: []
---

# Wrong revert reason In `onSlash` functionality

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-07-cyfrin-suzaku-core-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md)_

---

**Description:** In the `onSlash` function of `VaultTokenized`, the following check is used to validate the `captureEpoch` parameter:
```solidity
if ((currentEpoch_ > 0 && captureEpoch < currentEpoch_ - 1) || captureEpoch > currentEpoch_) {
    revert Vault__InvalidCaptureEpoch();
}
```
If `currentEpoch_` is 0, the expression `captureEpoch < currentEpoch_ - 1` will underflow, since `currentEpoch_ - 1` becomes less than 0. This will cause the check to revert with a generic arithmetic error instead of the intended custom error.

**Impact:** If `currentEpoch_` is 0, calling `onSlash` will cause an underflow in the comparison, resulting in a revert with a generic arithmetic error rather than the intended `Vault__InvalidCaptureEpoch` error. This can make debugging more difficult and may lead to unexpected behavior for callers.

**Recommended Mitigation:** Update the condition to avoid underflow by checking:
```solidity
if ((currentEpoch_ > 0 && captureEpoch + 1 < currentEpoch_) || captureEpoch > currentEpoch_) {
    revert Vault__InvalidCaptureEpoch();
}
```
This ensures the check is safe for all values of `currentEpoch_` and always reverts with the correct custom error when the input is invalid.

**Suzaku:**
Fixed in commit [b654dfb](https://github.com/suzaku-network/suzaku-core/commit/b654dfbb31dd6e840f2f7dfcda0f55dda3ff37b2).

**Cyfrin:** Verified.

\clearpage
