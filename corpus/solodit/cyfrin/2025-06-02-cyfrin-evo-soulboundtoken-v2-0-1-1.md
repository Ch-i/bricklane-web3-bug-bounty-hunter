---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-02-cyfrin-evo-soulboundtoken-v2-0-1-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-06-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-02-cyfrin-evo-soulboundtoken-v2.0.md
tags:
- firm:cyfrin
- report:2025-06-02-cyfrin-evo-soulboundtoken-v2-0
title: Assuming Chainlink price feed decimals can lead to unintended errors
vuln_class: []
---

# Assuming Chainlink price feed decimals can lead to unintended errors

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-02-cyfrin-evo-soulboundtoken-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-02-cyfrin-evo-soulboundtoken-v2.0.md)_

---

**Description:** In general, Chainlink x/USD price feeds use 8 decimal precision however this is not universally true for example [AMPL/USD](https://etherscan.io/address/0xe20CA8D7546932360e37E9D72c1a47334af57706#readContract#F3) uses 18 decimal precision.

Instead of [assuming Chainlink oracle price precision](https://medium.com/contractlevel/chainlink-oracle-defi-attacks-93b6cb6541bf#87fc), the precision variable could be declared `immutable` and initialized in the constructor via [`AggregatorV3Interface::decimals`](https://docs.chain.link/data-feeds/api-reference#decimals).

In practice though the price oracle is hard-coded in `script/HelperConfig.s.sol` and does use 8 decimals for on Optimism, so the current configuration will work fine.

**Evo:**
Fixed in commit [f594ae0](https://github.com/contractlevel/sbt/commit/f594ae004d4afc80f19e17c0f61d50caa00a4811).

**Cyfrin:** Verified.
