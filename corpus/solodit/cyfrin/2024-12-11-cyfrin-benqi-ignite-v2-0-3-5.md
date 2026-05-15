---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-11-cyfrin-benqi-ignite-v2-0-3-5
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-12-11T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-11-cyfrin-benqi-ignite-v2-0
title: Tokens with more than `18` decimals will not be supported
vuln_class: []
---

# Tokens with more than `18` decimals will not be supported

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-11-cyfrin-benqi-ignite-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md)_

---

**Description:** Currently, tokens with more than `18` decimals are not supported due to the decimals handling logic in [`StakingContract::_getPriceInUSD`](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L953):

```solidity
uint256 decimalDelta = uint256(18) - tokenDecimalDelta;
```

and [`Ignite::registerWithErc20Fee`:](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L299)

```solidity
uint tokenAmount = uint(avaxPrice) * registrationFee / uint(tokenPrice) / 10 ** (18 - token.decimals());
```

**Recommended Mitigation:** Modify this logic if tokens with a larger number of decimals are required to be supported.

**BENQI:** Acknowledged, working as expected.

**Cyfrin:** Acknowledged.
