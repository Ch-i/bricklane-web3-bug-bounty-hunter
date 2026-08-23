---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-1-8
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0
title: '`SecuritizeOnRamp` doesn''t provide a mechanism for investors to invalidate
  their nonces'
vuln_class: []
---

# `SecuritizeOnRamp` doesn't provide a mechanism for investors to invalidate their nonces

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md)_

---

**Description:** `SecuritizeOnRamp` has no function allowing investors to invalidate or increment their own nonce. The nonce only increments when `executePreApprovedTransaction` successfully executes.

**Impact:** If an investor signs an authorization and later changes their mind (market conditions changed, signed wrong parameters, etc.), they cannot cancel the pending authorization; the operator can still execute it.

**Recommended Mitigation:** Nonce implementations commonly provide a function for users to invalidate their nonces; for example OZ NoncesUpgradeable has a [_useNonce](https://github.com/OpenZeppelin/openzeppelin-contracts-upgradeable/blob/master/contracts/utils/NoncesUpgradeable.sol#L47) function which can be exposed to allow users to invalidate their own nonces.

**Securitize:** Acknowledged; at this time we don't want to expose user nonce validation for this particular functionality.
