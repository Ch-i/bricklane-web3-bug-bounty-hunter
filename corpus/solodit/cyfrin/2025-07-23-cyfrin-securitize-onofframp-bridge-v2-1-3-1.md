---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1-3-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-07-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1
title: Unnecessary override keywords on interface implementation functions
vuln_class: []
---

# Unnecessary override keywords on interface implementation functions

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md)_

---

**Description:** Multiple functions in the `SecuritizeOnRamp` contract use the `override` keyword unnecessarily. In Solidity, the `override` keyword is only required when overriding functions from parent contracts, not when implementing interface functions.

The following functions unnecessarily use the `override` keyword:
- `SecuritizeOnRamp::nonceByInvestor`
- `SecuritizeOnRamp::subscribe`
- `SecuritizeOnRamp::swap`
- `SecuritizeOnRamp::executePreApprovedTransaction`
- `SecuritizeOnRamp::calculateDsTokenAmount`
- `SecuritizeOnRamp::updateAssetProvider`
- `SecuritizeOnRamp::updateNavProvider`
- `SecuritizeOnRamp::updateMinSubscriptionAmount`
- `SecuritizeOnRamp::updateBridgeParams`
- `SecuritizeOnRamp::toggleInvestorSubscription`

**Impact:** The unnecessary `override` keywords create confusion about the contract's inheritance structure.

**Recommended Mitigation:** Remove the `override` keyword.

**Securitize:** Fixed in commit [bf7b87](https://github.com/securitize-io/bc-on-off-ramp-sc/commit/bf7b873d62fd346493c5726ea0a0726088926136).

**Cyfrin:** Verified.
