---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-02-cyfrin-syntetika-ccip-cct-v2-0-3-4
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
title: '`StakingVault::setDistributor` and `Minter::setDistributor` are independent
  - rotating one without the other silently bricks the yield pipeline'
vuln_class: []
---

# `StakingVault::setDistributor` and `Minter::setDistributor` are independent - rotating one without the other silently bricks the yield pipeline

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md)_

---

**Description:** Yield flow: `Distributor::distributeYield` -> `Minter::distributeYield` (requires `DISTRIBUTOR_ROLE` on Minter) -> `StakingVault::distributeYield` (requires `DISTRIBUTOR_ROLE` on Vault). Both Minter and StakingVault track the distributor address independently. Each `setDistributor` only rotates its own role binding. No atomic "replace distributor everywhere" helper. If admin rotates one side but not the other (or Minter's 2-step waits 1 day while Vault's is single-step), the yield pipeline reverts with role check failures.

Sources: issuance/src/vault/StakingVault.sol:138-148; issuance/src/minter/Minter.sol:301-319.

**Recommended Mitigation:** Document the co-requirement in NatSpec on both setters. Consider adding a governance helper that atomically drives both rotations (accepting that Minter's side is inherently 2-step after the Minter-side distributor-rotation fix).

**Syntetika:** Fixed in commit [`ff6434d`](https://github.com/SyntetikaLabs/monorepo/commit/ff6434ddb0fec4b8ab79f5ba8459866085d2fd91)

**Cyfrin:** Verified.
