---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-06-12-itrust-finance-0-3
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2021-06-12T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-12-iTrust%20Finance.md
tags:
- firm:zokyo
- report:2021-06-12-itrust-finance
title: Incorrect contracts used
vuln_class: []
---

# Incorrect contracts used

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2021-06-12-iTrust Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-12-iTrust%20Finance.md)_

---

**Description**

Some contracts inherit upgradeable contracts from OpenZeppelin contracts-upgradeable. So
it should use all utility contracts from the upgradeable set. For now incorrect contracts from
the “vanilla” set are used in a mixed case with upgradeable ones. Such approach can create
collisions, affect the development and create unpredictable issues in the runtime.
Vault.sol: IERC20, SafeMath and ECDSA
StakingData.sol: SafeMath
Burn.sol: SafeMath
BaseContract.sol: SafeMath
RoundData.sol: SafeMath
StakeData.sol: SafeMath

**Recommendation**:

Fix the contracts
