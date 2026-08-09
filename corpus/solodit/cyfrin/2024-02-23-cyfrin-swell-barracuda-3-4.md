---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-02-23-cyfrin-swell-barracuda-3-4
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-02-23T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md
tags:
- firm:cyfrin
- report:2024-02-23-cyfrin-swell-barracuda
title: Remove redundant pause checks
vuln_class: []
---

# Remove redundant pause checks

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-02-23-cyfrin-swell-barracuda.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md)_

---

**Description:** 1) Remove redundant `botMethodsPaused` [check](https://github.com/SwellNetwork/v3-contracts-lst/blob/a95ea7942ba895ae84845ab7fec1163d667bee38/contracts/implementations/swETH.sol#L208-L210) in `swETH::reprice` as:

* this function is only called by [`RepricingOracle::handleReprice`](https://github.com/SwellNetwork/v3-contracts-lst/blob/a95ea7942ba895ae84845ab7fec1163d667bee38/contracts/implementations/RepricingOracle.sol#L233)
* `RepricingOracle::handleReprice` can only be called by [`submitSnapshot`](https://github.com/SwellNetwork/v3-contracts-lst/blob/a95ea7942ba895ae84845ab7fec1163d667bee38/contracts/implementations/RepricingOracle.sol#L89-L94) and [`submitSnapshotV2`](https://github.com/SwellNetwork/v3-contracts-lst/blob/a95ea7942ba895ae84845ab7fec1163d667bee38/contracts/implementations/RepricingOracle.sol#L105-L112) which both already contain the `botMethodsPaused` check.

2) Remove redundant `withdrawalsPaused` [check](https://github.com/SwellNetwork/v3-contracts-lst/blob/a95ea7942ba895ae84845ab7fec1163d667bee38/contracts/implementations/swEXIT.sol#L117-L119) in `swEXIT::processWithdrawals` as this function is only supposed to be callable by `RepricingOracle` which already [contains](https://github.com/SwellNetwork/v3-contracts-lst/blob/a95ea7942ba895ae84845ab7fec1163d667bee38/contracts/implementations/RepricingOracle.sol#L129) the check.

**Swell:** Fixed in commits [1fca965](https://github.com/SwellNetwork/v3-contracts-lst/commit/1fca965019facc4dcc79c35bfc45c8a711043196), [3f85df3](https://github.com/SwellNetwork/v3-contracts-lst/commit/3f85df3ba0e91b26e4234b15ad94f492fa6d46ec).

**Cyfrin:**
Verified.
