---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-11-cyfrin-benqi-ignite-v2-0-3-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-12-11T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-11-cyfrin-benqi-ignite-v2-0
title: Missing `onlyInitializing` modifier in `StakingContract`
vuln_class: []
---

# Missing `onlyInitializing` modifier in `StakingContract`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-11-cyfrin-benqi-ignite-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md)_

---

**Description:** While it is not currently possible for the functions to be invoked elsewhere, both [`StakingContract::initializeRoles`](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L152) and [`StakingContract::setInitialParameters`](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L185) should be limited to being called during initialization but are missing the `onlyInitializing` modifier. Note that the latter is however handled by its [internal call](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L222-228) to [`StakingContract::_initializePriceFeeds`](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L286) that does have it applied.

**Recommended Mitigation:** Consider adding the `onlyInitializing` modifier to `StakingContract::initializeRoles` and possibly also `StakingContract::setInitialParameters`.

**BENQI:** Fixed in commit [cd4d43e](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/commit/cd4d43ea8397357b503a127d7ac7966b625a21b7).

**Cyfrin:** Verified. The modifier has been added.
