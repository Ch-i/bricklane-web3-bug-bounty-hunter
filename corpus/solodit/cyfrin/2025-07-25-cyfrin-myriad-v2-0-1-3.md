---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-25-cyfrin-myriad-v2-0-1-3
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-07-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-25-cyfrin-myriad-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-25-cyfrin-myriad-v2-0
title: Disallow single-outcome markets
vuln_class: []
---

# Disallow single-outcome markets

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-25-cyfrin-myriad-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-25-cyfrin-myriad-v2.0.md)_

---

**Description:** When creating a market in [`PredictionMarketV3_4::_createMarket`](https://github.com/Polkamarkets/polkamarkets-js/blob/24f1394be94d27433d2e3a7370442126e1c1e5ba/contracts/PredictionMarketV3_4.sol#L299-L356), the following [check](https://github.com/Polkamarkets/polkamarkets-js/blob/24f1394be94d27433d2e3a7370442126e1c1e5ba/contracts/PredictionMarketV3_4.sol#L311) ensures that the number of outcomes is within bounds:

```solidity
require(desc.outcomes > 0 && desc.outcomes <= MAX_OUTCOMES, "!oc");
```

However, allowing `desc.outcomes == 1` results in a prediction market with only one possible outcome, which undermines the purpose of having a market at all.

Consider changing the check to:

```solidity
require(desc.outcomes > 1 && desc.outcomes <= MAX_OUTCOMES, "!oc");
```

to ensure that all created markets include at least two outcomes.

**Myriad:** Fixed in [PR#78](https://github.com/Polkamarkets/polkamarkets-js/pull/78), commit [`9d0090d`](https://github.com/Polkamarkets/polkamarkets-js/pull/78/commits/9d0090d43085cca20b955cbddc33d928619c8f32)

**Cyfrin:** Verified. Check for outcomes is not `>= 2`.
