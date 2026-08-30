---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-11-cyfrin-benqi-ignite-v2-0-3-12
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
title: Misalignment of `pause()` and `unpause()` access controls across contracts
vuln_class: []
---

# Misalignment of `pause()` and `unpause()` access controls across contracts

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-11-cyfrin-benqi-ignite-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md)_

---

**Description:** All three contracts, `Ignite`, `ValidatorRewarder`, and `StakingContract`, have pausing functionality that can be triggered by accounts with special privileges; however, they all implement the access control differently:

- In `Ignite`, [`pause()`](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L709-L716) can only be called by accounts granted the `ROLE_PAUSE` role and similarly for [`unpause()`](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L718-L725) it is the `ROLE_UNPAUSE` role.

- In `ValidatorRewarder`, both [`pause()`](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/ValidatorRewarder.sol#L126-L135) and [`unpause()`](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/ValidatorRewarder.sol#L137-L146) can only be called by accounts granted the `ROLE_PAUSE` role. The role `ROLE_UNPAUSE` is [defined](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/ValidatorRewarder.sol#L22) but not used.

- In `StakingContract`, both [`pause()`](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L627-L632) and [`unpause()`](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L634-L639) are limited to accounts granted the role `DEFAULT_ADMIN_ROLE`.

**Recommended Mitigation:** Consider aligning the role configuration between all contracts, preferably using the `ROLE_PAUSE`/`ROLE_UNPAUSE` setup from `Ignite` as it gives the most flexibility.

**BENQI:** Acknowledged, won’t change.

**Cyfrin:** Acknowledged.
