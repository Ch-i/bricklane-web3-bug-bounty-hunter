---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-11-cyfrin-benqi-ignite-v2-0-3-1
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
title: Unchained initializers should be called instead
vuln_class: []
---

# Unchained initializers should be called instead

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-11-cyfrin-benqi-ignite-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md)_

---

**Description:** While not an immediate issue in the current implementation, the direct use of initializer functions rather than their unchained equivalents should be avoided. [`ValidatorRewarder::initialize`](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/ValidatorRewarder.sol#L51-L52) and [`StakingContract::initialize`](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L259-261) should be modified to avoid [potential duplicate initialization](https://docs.openzeppelin.com/contracts/5.x/upgradeable#multiple-inheritance) in the future.

Note that this is also relevant for [`Ignite::initialize`](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L132-134), but since the contract is already initialized it is of no concern.

**Recommended Mitigation:** Consider using unchained initializers in `ValidatorRewarder::initialize`, `StakingContract::initialize`, and possibly also in `Ignite::initialize`.

**BENQI:** Fixed in commit [cd4d43e](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/commit/cd4d43ea8397357b503a127d7ac7966b625a21b7).

**Cyfrin:** Verified. Unchained initializers are now used.
