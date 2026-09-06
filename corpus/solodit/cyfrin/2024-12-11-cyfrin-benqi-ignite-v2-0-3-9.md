---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-11-cyfrin-benqi-ignite-v2-0-3-9
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-12-11T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-11-cyfrin-benqi-ignite-v2-0
title: Incorrect assumption that Chainlink price feeds will always have the same decimals
vuln_class: []
---

# Incorrect assumption that Chainlink price feeds will always have the same decimals

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-11-cyfrin-benqi-ignite-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md)_

---

**Description:** There are several instances [[1](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L227), [2](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L299), [3](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L381)] in `Ignite` where the decimal precision of Chainlink price feeds are assumed to be equal. Currently, this does not cause any issues as both `AVAX`, `QI`, and all other `USD` feeds return prices with `8` decimal precision, but this should be handled explicitly as `ETH` feeds return prices with `18` decimal precision as explained [here](https://ethereum.stackexchange.com/questions/92508/do-all-chainlink-feeds-return-prices-with-8-decimals-of-precision).

**Recommended Mitigation:** Consider explicit handling of Chainlink price feed decimals.

**BENQI:** Acknowledged, USD feeds always have eight decimals.

**Cyfrin:** Acknowledged.
