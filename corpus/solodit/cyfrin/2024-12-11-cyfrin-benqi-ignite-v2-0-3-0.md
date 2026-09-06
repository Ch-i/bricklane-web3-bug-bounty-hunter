---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-11-cyfrin-benqi-ignite-v2-0-3-0
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
title: '`AccessControlUpgradeable::_setupRole` is deprecated'
vuln_class: []
---

# `AccessControlUpgradeable::_setupRole` is deprecated

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-11-cyfrin-benqi-ignite-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md)_

---

**Description:** In [`ValidatorRewarder::initialize`](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/ValidatorRewarder.sol#L38-L59) the `DEFAULT_ADMIN_ROLE` is assigned using [`AccessControlUpgradeable::_setupRole`](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/ValidatorRewarder.sol#L54):

```solidity
_setupRole(DEFAULT_ADMIN_ROLE, _admin);
```

This method has been deprecated by OpenZeppelin in favor of the `AccessControlUpgradeable::_grantRole` as written in their [documentation](https://docs.openzeppelin.com/contracts/4.x/api/access#AccessControl-_setupRole-bytes32-address-) and NatSpec:

```solidity
/**
 * @dev Grants `role` to `account`.
 * ...
 * NOTE: This function is deprecated in favor of {_grantRole}.
 */
function _setupRole(bytes32 role, address account) internal virtual {
    _grantRole(role, account);
}
```

Note that `Ignite::initialize` [also uses this](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L136), but since the contract is already initialized it is of no concern.

**Recommended Mitigation:** Consider using `AccessControlUpgradeable::_grantRole` in `ValidatorRewarder::initialize`, and possibly also in `Ignite::initialize`.

**BENQI:** Fixed in commit [8db7fb5](https://github.com/Benqi-fi/ignite-contracts/commit/8db7fb5d4c27be03aa8c48437a17d9cca3bbc32d).

**Cyfrin:** Verified.
