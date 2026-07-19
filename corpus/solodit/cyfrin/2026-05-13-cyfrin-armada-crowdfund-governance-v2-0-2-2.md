---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-2-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-05-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-13-cyfrin-armada-crowdfund-governance-v2-0
title: '`ArmadaGovernor::setExcludedAddresses` lacks deduplication - quorum floor
  collapse via duplicate'
vuln_class: []
---

# `ArmadaGovernor::setExcludedAddresses` lacks deduplication - quorum floor collapse via duplicate

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** `ArmadaGovernor::setExcludedAddresses` pushes entries onto `_excludedFromQuorum` without checking for duplicates or using a set-membership mapping. A duplicate entry that corresponds to a large-balance address doubles that balance in every future `_initProposal`'s `excludedBalance` summation. The `excludedBalance > totalSupply` cap at line 862 clamps the sum to `totalSupply`, pinning `snapshotEligibleSupply = 0` and collapsing the percentage-based quorum to zero. `quorum()` then falls back to `QUORUM_FLOOR = 100k ARM`. Because `excludedAddressesLocked` is one-way, the misconfiguration is permanent.

**Impact:** A single deployer typo (e.g. listing the crowdfund twice) permanently collapses the quorum to the 100k ARM floor. Recovery requires a UUPS upgrade, which itself depends on the collapsed quorum - a bootstrap problem.

**Recommended Mitigation:** Track set membership via a mapping and reject duplicates:

```solidity
mapping(address => bool) private _isExcluded;

for (uint256 i = 0; i < addrs.length; i++) {
    require(!_isExcluded[addrs[i]], "Gov: duplicate excluded");
    _isExcluded[addrs[i]] = true;
    _excludedFromQuorum.push(addrs[i]);
}
```

**Armada:** Fixed in commit [2762a72](https://github.com/ship-armada/armada-poc/commit/2762a72ec8d1a1ce0b876774b6076981939b960d) by looping through and checking all existing entries to prevent duplicates.

**Cyfrin:** Verified.
