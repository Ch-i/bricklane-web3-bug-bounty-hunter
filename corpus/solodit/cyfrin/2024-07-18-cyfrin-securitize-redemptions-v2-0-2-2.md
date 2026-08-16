---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-18-cyfrin-securitize-redemptions-v2-0-2-2
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-07-18T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-18-cyfrin-securitize-redemptions-v2.0.md
tags:
- firm:cyfrin
- report:2024-07-18-cyfrin-securitize-redemptions-v2-0
title: Lack of a feature to allow investors to increase their nounce
vuln_class: []
---

# Lack of a feature to allow investors to increase their nounce

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-18-cyfrin-securitize-redemptions-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-18-cyfrin-securitize-redemptions-v2.0.md)_

---

**Description:** The function `SecuritizeSwap::executePreApprovedTransaction()` allows anyone to execute a pre-approved transaction by providing a valid signature.
This function relies on an internal function `doExecuteByInvestor()` and the hash is calculated based on various attributes including the investor's nonce.
This nonce mechanism is in place to prevent executing the same transaction.
Generally, nonce mechanism comes with an invalidation mechanism together so that the nonce owner can invalidate the current nonce by increasing the nonce proactively.
The current design does not provide a way to increase the nonce and this means an investor can not invalidate an already signed hash.

**Impact:** The investors do not have a way to invalidate already signed hashes.

**Recommended Mitigation:** Add a function where an investor can increase their nonce to invalidate the already signed hashes.

**Securitize:** We will not apply this suggestion because the investor cannot modify their nonce.
This will only be done with the contract and our backend. Additionally, NAV Rate changes will be controlled.

**Cyfrin:** Acknowledged.
