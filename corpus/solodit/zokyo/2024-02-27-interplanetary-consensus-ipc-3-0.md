---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-02-27-interplanetary-consensus-ipc-3-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-02-27T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md
tags:
- firm:zokyo
- report:2024-02-27-interplanetary-consensus-ipc
title: Exposure to Reentrance
vuln_class: []
---

# Exposure to Reentrance

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-02-27-InterPlanetary Consensus (IPC).md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

SubnetActorManagerFacet.sol - Function `unstake()` is exposed to reentrancy as well as cross-function reentrancy. The reentrancy is can be triggered when the execution reaches `LibStaking.withdrawWithConfirm(msg.sender, amount);`. The severity of this finding is not serious because the function adheres to checks-effects-interactions pattern, hence no scenario found in which the attacker would be incentivised to exploit a reentancy to acquire any sort of unjust gain.
```solidity
   function unstake(uint256 amount) external whenNotPaused notKilled {
        // disbling validator changes for federated validation subnets (at least for now
        // until a more complex mechanism is implemented).
        enforceCollateralValidation();

        if (amount == 0) {
            revert CannotReleaseZero();
        }

        uint256 collateral = LibStaking.totalValidatorCollateral(msg.sender);

        if (collateral == 0) {
            revert NotValidator(msg.sender);
        }
        if (collateral <= amount) {
            revert NotEnoughCollateral();
        }
        if (!s.bootstrapped) {
            LibStaking.withdrawWithConfirm(msg.sender, amount);
            return;
        }

        LibStaking.withdraw(msg.sender, amount);
    }
```

**Recommendation** 

Apply reentrancy guard.

**Fix**: Issue addressed and resolved according to recommendation in commit 9a663e5 .
