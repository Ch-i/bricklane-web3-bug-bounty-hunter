---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-11-cyfrin-benqi-ignite-v2-0-3-13
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-12-11T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-11-cyfrin-benqi-ignite-v2-0
title: Inconsistent price validation in `Ignite::registerWithStake`
vuln_class: []
---

# Inconsistent price validation in `Ignite::registerWithStake`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-11-cyfrin-benqi-ignite-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md)_

---

**Description:** In [`Ignite::registerWithErc20Fee`](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L294), [`Ignite::registerWithPrevalidatedQiStake`](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L376), and [`StakingContract::_getPriceInUSD`](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L939-942), prices are validated to be greater than `0`; however, in [`Ignite::registerWithStake`](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L221), the `AVAX` price is validated to be greater than the `QI` price. While the `AVAX` price is currently significantly higher than the `QI` price and so will not result in any unwanted reverts, this validation is inconsistent with the other instances and should be modified.

**Recommended Mitigation:** Modify the validation to require the `AVAX` price to be greater than `0` instead of the `QI` price.

**BENQI:** Acknowledged, won’t change.

**Cyfrin:** Acknowledged.

\clearpage
