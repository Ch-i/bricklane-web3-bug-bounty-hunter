---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-19-cyfrin-stakepet-2-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-09-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-stakepet.md
tags:
- firm:cyfrin
- report:2023-09-19-cyfrin-stakepet
title: Closedown condition is inconsistent with the stated documentation of majority
  agreement
vuln_class: []
---

# Closedown condition is inconsistent with the stated documentation of majority agreement

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-19-cyfrin-stakepet.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-stakepet.md)_

---

**Severity:** Low

**Description:** [Documentation](https://hackmd.io/CPINxScvSE2vo-t8mwY_Og#Risks) states the following:

_"Closing the Contract: If the majority of the pets agree, they can vote to close the contract. Once closed, the remaining funds will be divided among the surviving pets. This is the most beneficial scenario for you, as you’ll earn the base rewards, early withdrawal rewards, and rewards from dead pets."_

Inline comments for the [`StakePet::closedown`](https://github.com/Ranama/StakePet/blob/9ba301823b5062d657baa3462224da498dc4bb46/src/StakePet.sol#L398C2-L398C2) function state the following"

```
    /// @notice Close down the contract if majority wants it, after closedown everyone can withdraw without getting a yield cut and no pet can die.
    function closedown(uint256[] memory _idsOfMajorityThatWantsClosedown) external {
...
}
```

In both cases, condition for closedown is for `majority of pets` to agree for a closedown. However, the check used for `closedown` is that the total collateral of pets wanting a closedown should be atleast 50% of the total collateral. This would mean that a single or few pet owners with large collateral deposits can trigger a closedown even if its not something that a majority of pet owners agree to.

Having 50% of value agreement and having majority agreement could be 2 different things.

**Impact:** The current model can be hijacked by whales who can trigger closedown of contract whenever they wish to. This could create a bad user experience for majority of pet owners who want to stay in the contract

**Recommended Mitigation:** Please make documentation consistent with the vision for stake pets.

**Client:** Fixed in [54a4dcb](https://github.com/Ranama/StakePet/commit/54a4dcbb696da3138dc0fdd8e7032d664d32b7da)

**Cyfrin:** Verified.
