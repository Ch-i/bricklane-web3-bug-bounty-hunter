---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-21-cyfrin-chaos-labs-risk-oracle-v2-0-1-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-08-21T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-21-cyfrin-chaos-labs-risk-oracle-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-21-cyfrin-chaos-labs-risk-oracle-v2-0
title: Asymmetry in validation between `RiskOracle::addUpdateType` and contract constructor
vuln_class: []
---

# Asymmetry in validation between `RiskOracle::addUpdateType` and contract constructor

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-21-cyfrin-chaos-labs-risk-oracle-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-21-cyfrin-chaos-labs-risk-oracle-v2.0.md)_

---

**Description:** The following [validation](https://github.com/ChaosLabsInc/risk-oracle/blob/9449219174e3ee7da9a13a5db7fb566836fb4986/src/RiskOracle.sol#L92) is present within `RiskOracle::addUpdateType`:
```solidity
require(!validUpdateTypes[newUpdateType], "Update type already exists.");
```
However, this function has the `onlyOwner` modifier applied, so the validation is not strictly necessary. This can be observed within the constructor, invoked when the owner deploys the contract, where there is no such validation – here, it is assumed that duplicates will be checked off-chain. As such, there is an asymmetry between these two instances that is recommended to be made consistent by either completely removing the validation or having it present in both code paths.

**Chaos Labs:** Added duplicate check in constructor in commit [9f7375a](https://github.com/ChaosLabsInc/risk-oracle/commit/9f7375a8291deb04719ec4ddbfff1eb638db55e1).

**Cyfrin:** Verified, the duplicate check has been added to the constructor.
