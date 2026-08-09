---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-17-cyfrin-remora-final-v2-0-2-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-11-17T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-17-cyfrin-remora-final-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-17-cyfrin-remora-final-v2-0
title: Unnecessary usage of `nonReentrant` modifier on `ReferralManager::completeFirstPurchase`
vuln_class: []
---

# Unnecessary usage of `nonReentrant` modifier on `ReferralManager::completeFirstPurchase`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-17-cyfrin-remora-final-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-17-cyfrin-remora-final-v2.0.md)_

---

**Description:** `ReferralManager::completeFirstPurchase` has in place the `nonReentrant` modifier from the `ReentrancyGuardTransientUpgradeable` library, but this function is not susceptible to reentrancy.
- The caller is restricted to be the `TokenBank` contract, and the only external call is to do a transfer of stablecoin to the referrer.

As long as the stablecoin is set correctly to a valid contract, there is no need to use the `nonReentrant` modifier.

**Recommended Mitigation:** `nonReentrant` modifier is not required. Remove the import of `ReentrancyGuardTransientUpgradeable` library.

**Remora**
Fixed in commit [59a33a4](https://github.com/remora-projects/remora-dynamic-tokens/commit/59a33a40bfcdc585d5a24a58108fcd4f2e583a05)

**Cyfrin:** Verified.

\clearpage
