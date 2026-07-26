---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-02-cyfrin-syntetika-ccip-cct-v2-0-2-7
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-05-02T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-02-cyfrin-syntetika-ccip-cct-v2-0
title: Missing runtime input validation on admin setters and creator-role functions
vuln_class: []
---

# Missing runtime input validation on admin setters and creator-role functions

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md)_

---

**Description:** Several admin setters validate only lower bounds, or nothing:

- `Minter::updateWaitingPeriod`, `HilToken::updateWaitingPeriod`: only `>= MIN_REQUEST_WAITING_PERIOD`. Setting to `type(uint256).max` overflows every 2-step check, bricking upgrades. Because the upgrade path uses the same `waitingPeriod`, recovery via upgrade is impossible.
- `Distributor::updateTimeLock`: only `> 0`. Extreme values freeze `distributeYield` and make `getUnvestedAmount` never-vest; `Minter`'s `require(getUnvestedAmount() == 0)` guard then rejects all future yield calls.
- `StakingVault::setMinAssetsAmount`: no bounds. `type(uint256).max` reverts every deposit and new unstake with `AmountBelowLimit`.

**Impact:** Under a compromised admin, DoS of upgrades, yield pipeline, deposits/withdrawals, and onboarding. Some variants are unrecoverable without upgrade because the setter that protects the cap is itself affected by the cap.

**Recommended Mitigation:** Add reasonable upper bounds, e.g. `MAX_REQUEST_WAITING_PERIOD = 30 days`, `MAX_TIME_LOCK = 30 days`, `MAX_MIN_ASSETS_AMOUNT = 10 ** asset.decimals()`, `MAX_CHALLENGE_PERIOD = 30 days`.


**Syntetika:** Fixed in commit [`33bc4ea`](https://github.com/SyntetikaLabs/monorepo/commit/33bc4ea56421e08be856818e4ccb3f689f2a6b73). For compliant deposit registry - contract is deprecated, so OOS

**Cyfrin:** Verified.
