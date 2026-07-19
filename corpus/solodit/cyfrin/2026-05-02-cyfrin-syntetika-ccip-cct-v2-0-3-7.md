---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-02-cyfrin-syntetika-ccip-cct-v2-0-3-7
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-05-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-02-cyfrin-syntetika-ccip-cct-v2-0
title: Missing NatSpec on public-facing functions with non-obvious behaviour
vuln_class: []
---

# Missing NatSpec on public-facing functions with non-obvious behaviour

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md)_

---

**Description:** Public/external functions with surprise-potential semantics lack documentation. In particular `HilToken::requestTransfer` has no NatSpec and no access control; `StakingVault::redeem` and `StakingVault::withdraw` ignore owner/receiver params - NatSpec does not mention this; `StakingVault::getEarlyExitAmount` percent/fee math is non-obvious.

**Recommended Mitigation:** Add NatSpec stating (a) that `redeem`/`withdraw` ignore the passed owner/receiver addresses and always operate on `msg.sender`, and (b) unit conventions for `getEarlyExitAmount` (BPS, linear interpolation, etc.).

**Syntetika:** Fixed in commit [`6d1e8e0`](https://github.com/SyntetikaLabs/monorepo/commit/6d1e8e0c40e863a58cfb861db5c5630ac4700c1d)

**Cyfrin:** Verified. `redeem`/`withdraw` use `owner`/`receiver` params as expected and `StakingVault::getEarlyExitAmount` perfent/fee math is documented in natspec.
