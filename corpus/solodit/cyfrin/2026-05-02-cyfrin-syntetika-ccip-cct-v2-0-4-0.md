---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-02-cyfrin-syntetika-ccip-cct-v2-0-4-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-05-02T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-02-cyfrin-syntetika-ccip-cct-v2-0
title: Cache repeated storage reads on success path across multiple setters
vuln_class: []
---

# Cache repeated storage reads on success path across multiple setters

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md)_

---

**Description:** Several functions re-read the same storage slot multiple times on the success path. Caching in a local saves ~100 gas per subsequent warm SLOAD:
- `Minter::setDistributor` (`$.distributor` read on initial check then again in `_revokeRole`)
- `HilToken::setMinter` (`$.minter` read twice)
- `StakingVault::redeem` (`$.cooldowns[msg.sender]` written 3 times)
- `StakingVault::withdraw` (`$.cooldowns[msg.sender]` accessed 4x, `$.cooldownDuration` read twice)
- `StakingVault::claimWithdraw` (`$.tokensHolder` read up to 3 times)

**Recommended Mitigation:** Cache the storage slot or storage pointer into a local (e.g., `address _distributor = $.distributor;`, `UserCooldown storage userCooldown = $.cooldowns[msg.sender];`) and reuse it.

**Syntetika:** Fixed in commit [`340b912`](https://github.com/SyntetikaLabs/monorepo/commit/340b9129ec5c5b96c2eaeb3682a731b52268bcb0)

**Cyfrin:** Verified.
