---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-18-cyfrin-securitize-redemptions-v2-0-3-4
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-07-18T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-18-cyfrin-securitize-redemptions-v2.0.md
tags:
- firm:cyfrin
- report:2024-07-18-cyfrin-securitize-redemptions-v2-0
title: Missing zero check for the result of `ecrecover()`
vuln_class: []
---

# Missing zero check for the result of `ecrecover()`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-18-cyfrin-securitize-redemptions-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-18-cyfrin-securitize-redemptions-v2.0.md)_

---

**Description:** The function `SecuritizeSwap::doExecuteByInvestor()` validates the provided signature was actually signed by an actor with a role `ROLE_ISSUER` or `ROLE_MASTER`.
In the validation, `ecrecover()` is used but the result is not validated to be non-zero.
Although, it is understood that the following line validates the role of the `recovered`, it is strongly recommended to implement this check for unexpected problems in the future.



**Securitize:** Fixed in commit [b09460](https://bitbucket.org/securitize_dev/securitize-swap/commits/b094604b341123a49c8abbd6e1c3d53d7c102f28)

**Cyfrin:** Verified.
