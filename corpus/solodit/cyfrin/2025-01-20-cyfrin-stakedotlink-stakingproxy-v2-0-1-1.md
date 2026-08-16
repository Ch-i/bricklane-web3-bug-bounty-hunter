---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-01-20-cyfrin-stakedotlink-stakingproxy-v2-0-1-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-01-20T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-01-20-cyfrin-stakedotlink-stakingproxy-v2.0.md
tags:
- firm:cyfrin
- report:2025-01-20-cyfrin-stakedotlink-stakingproxy-v2-0
title: Storage collision risk in UUPS upgradeable `StakingProxy` due to missing storage
  gap
vuln_class: []
---

# Storage collision risk in UUPS upgradeable `StakingProxy` due to missing storage gap

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-01-20-cyfrin-stakedotlink-stakingproxy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-01-20-cyfrin-stakedotlink-stakingproxy-v2.0.md)_

---

**Description:** `StakingProxy` contract inherits from `UUPSUpgradeable` and `OwnableUpgradeable` but does not implement storage gaps to protect against storage collisions during upgrades.

`StakingProxy` is intended to be used by third parties/DAOs. It is possible that this contract gets inherited by external contracts with their own storage variables. In such a scenario, adding new storage variables to `StakingProxy` during an upgrade can shift storage slots and cause serious storage collision risks.


`StakingProxy.sol`
```solidity
contract StakingProxy is UUPSUpgradeable, OwnableUpgradeable {
    // address of asset token
    IERC20Upgradeable public token;
    // address of liquid staking token
    IStakingPool public lst;
    // address of priority pool
    IPriorityPool public priorityPool;
    // address of withdrawal pool
    IWithdrawalPool public withdrawalPool;
    // address of SDL pool
    ISDLPool public sdlPool;
    // address authorized to deposit/withdraw asset tokens
    address public staker; // ---> @audit missing storage slots
}
```

**Impact:** Potential storage collision can corrupt data and cause contract to malfunction.

**Recommended Mitigation:** Consider adding a storage gap at the end of the contract to reserve slots for future inherited contract variable. A slot size of 50 is the [OpenZeppelin's recommended pattern](https://docs.openzeppelin.com/contracts/3.x/upgradeable#:~:text=Storage%20Gaps,with%20existing%20deployments.) for upgradeable contracts.

**Stake.link:**
Acknowledged.

**Cyfrin:** Acknowledged.

\clearpage
