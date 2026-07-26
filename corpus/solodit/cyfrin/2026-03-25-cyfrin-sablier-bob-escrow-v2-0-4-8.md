---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-4-8
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-03-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-25-cyfrin-sablier-bob-escrow-v2-0
title: Consider adding a vault migration feature so non-adapter vault users can migrate
  to a vault with an adapter
vuln_class: []
---

# Consider adding a vault migration feature so non-adapter vault users can migrate to a vault with an adapter

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md)_

---

**Description:** When a vault is created using `SablierBob::createVault`, the adapter for the `vaultId` is retrieved from the `_defaultAdapters` mapping, which can store both a zero or non-zero value. The issue is that if an adapter is added after a user has created and deposited into a vault, the user loses out on potential yield from that adapter.

For example:
 - Alice creates a vault for WBTC token with an expiry 3 years from the current timestamp.
 - After 1 month, the team decides to add an adapter for the WBTC token.
 - Bob, Charlie and other users create another vault for the WBTC token and deposit in it to earn yield from the adapter that provides 6% returns annually.
 - Alice is locked for 3 years with no interest.

This can create user dissatisfaction since multiple users could be locked for years or decades in vaults that do not generate yield currently but may in the future with adapter integrations.

**Recommended Mitigation:** Consider implementing functionality that allows existing non-adapter vaults to migrate and earn yield.

**Sablier:** Acknowledged; may be added in a future version.

\clearpage
