---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-02-23-cyfrin-swell-barracuda-1-3
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-02-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md
tags:
- firm:cyfrin
- report:2024-02-23-cyfrin-swell-barracuda
title: Check for staleness of data when fetching Proof of Reserves via Chainlink `Swell
  ETH PoR` Oracle
vuln_class: []
---

# Check for staleness of data when fetching Proof of Reserves via Chainlink `Swell ETH PoR` Oracle

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-02-23-cyfrin-swell-barracuda.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md)_

---

**Description:** `RepricingOracle::_assertRepricingSnapshotValidity` [uses](https://github.com/SwellNetwork/v3-contracts-lst/tree/a95ea7942ba895ae84845ab7fec1163d667bee38/contracts/implementations/RepricingOracle.sol#L329-L331) the `Swell ETH PoR` Chainlink Proof Of Reserves Oracle to fetch an off-chain data source for Swell's current reserves.

The Oracle `Swell ETH PoR` is [listed](https://docs.chain.link/data-feeds/proof-of-reserve/addresses?network=ethereum&page=1#networks) on Chainlink's website as having a heartbeat of `86400` seconds (check the "Show More Details" box in the top-right corner of the table), however [no staleness check](https://medium.com/SwellNetwork/chainlink-oracle-defi-attacks-93b6cb6541bf#99af) is implemented by `RepricingOracle`:
```solidity
// @audit no staleness check
(, int256 externallyReportedV3Balance, , , ) = AggregatorV3Interface(
  ExternalV3ReservesPoROracle
).latestRoundData();
```

**Impact:** If the `Swell ETH PoR` Chainlink Proof Of Reserves Oracle has stopped functioning correctly, `RepricingOracle::_assertRepricingSnapshotValidity` will continue processing with stale reserve data as if it were fresh.

**Recommended Mitigation:** Implement a staleness check and if the Oracle is stale, either revert or skip using it as the code currently does [if the oracle is not set](https://github.com/SwellNetwork/v3-contracts-lst/tree/a95ea7942ba895ae84845ab7fec1163d667bee38/contracts/implementations/RepricingOracle.sol#L325-L327).

For multi-chain deployments ensure that a [correct staleness check is used for each feed](https://medium.com/SwellNetwork/chainlink-oracle-defi-attacks-93b6cb6541bf#fb78) as the same feed can have different heartbeats on different chains.

Consider adding an off-chain bot that periodically checks if the Oracle has become stale and if it has, raises an internal alert for the team to investigate.

**Swell:** Fixed in commit [84a6517](https://github.com/SwellNetwork/v3-contracts-lst/commit/84a65178c31222d80559f6fd5f1b4c60f9249016).

**Cyfrin:**
Verified.
