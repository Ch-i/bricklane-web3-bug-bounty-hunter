---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-02-cyfrin-syntetika-ccip-cct-v2-0-1-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-05-02T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-02-cyfrin-syntetika-ccip-cct-v2-0
title: '`Distributor::distributeYield` permissionless + no `yieldAmount` validation
  - griefing burns rate-limit slot'
vuln_class: []
---

# `Distributor::distributeYield` permissionless + no `yieldAmount` validation - griefing burns rate-limit slot

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md)_

---

**Description:** `distributeYield` is permissionless (by design, rate-limited by `timeLock`). It forwards `feed.getYieldAmount()` unchecked. If the feed transiently returns 0 (e.g., between `updateFeed` and feed heartbeat, or by design in low-yield periods), an attacker or any bot can:

1. Call `distributeYield()` - `yieldAmount = 0` minted, `lastDistribution = block.timestamp`.
2. Legitimate distribution is now locked out for `timeLock` seconds. The real yield accrued during that window is lost (feed is non-cumulative).

Additionally: on the first call, `lastDistribution == 0` makes the rate-limit trivially pass, so a griefer can race the first legitimate call.

Source: `issuance/src/vault/Distributor.sol:122-131`.

**Impact:** Griefing that deprives stakers of one `timeLock` epoch of yield per occurrence. Repeatable on every feed transition. Feed integration is future-work (known issue), but the permissionless-caller design with no `yieldAmount > 0` check is a contract-side bug that survives any feed choice.

**Recommended Mitigation:** Add `require(yieldAmount > 0, ZeroYield())`. Consider gating `distributeYield` behind a loose role (keeper). Initialize `lastDistribution = block.timestamp` in `initialize` so first-call also respects the cadence.

**Syntetika:** Fixed in commit [`ace7bea`](https://github.com/SyntetikaLabs/monorepo/commit/ace7beafcb6c4f917009da23968ea0e84bfcee6d)

**Cyfrin:** Verified. Call reverts if yield is 0.


\clearpage
