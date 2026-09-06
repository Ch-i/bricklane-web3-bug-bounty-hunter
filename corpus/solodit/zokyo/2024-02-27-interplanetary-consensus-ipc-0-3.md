---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-02-27-interplanetary-consensus-ipc-0-3
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-02-27T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md
tags:
- firm:zokyo
- report:2024-02-27-interplanetary-consensus-ipc
title: Validators with dust collateral can join the network
vuln_class: []
---

# Validators with dust collateral can join the network

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2024-02-27-InterPlanetary Consensus (IPC).md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md)_

---

**Severity**: High

**Status**: Acknowledged

SubnetActorManagerFacet.sol - In join function , validators are allowed to join the network to be added to `genesisValidators` in exchange for dust values as low as 1 native coin. This in turn can flood the `s.genesisValidators` array. There is a minimum stake mechanism (i.e. `s.minActivationCollateral` ) but it is meant for bootstrapping the subnet. Validators though can be added arbitrarily while the subnet is not bootstrapped yet. The only cost hindering this spamming of validators is the gas cost.
It is worth noting that a large number of `genesisValidators` adds up to the size of the for loop in `LibStaking.depositWithConfirm` function as shown in the following:

```solidity
   function depositWithConfirm(address validator, uint256 amount) internal {
        ...
        if (!s.bootstrapped) {
            // add to initial validators avoiding duplicates if it
            // is a genesis validator.
            bool alreadyValidator;
            uint256 length = s.genesisValidators.length;
            for (uint256 i; i < length; ) {
                if (s.genesisValidators[i].addr == validator) {
                    alreadyValidator = true;
                    break;
                }
                unchecked {
                    ++i;
                }
            }
            if (!alreadyValidator) {
                uint256 collateral = s.validatorSet.validators[validator].confirmedCollateral;
                Validator memory val = Validator({
                    addr: validator,
                    weight: collateral,
                    metadata: s.validatorSet.validators[validator].metadata
                });
                s.genesisValidators.push(val);
            }
        }
    }
```
This increases the gas cost of the operation as more spammed `genesisValidators` are added up. Also there is a potential risk of denial-of-service if the for loop is exceedingly big (ps. not a likely scenario due to the gas cost that will be incurred on attacker to add up many validators).
Similarly this issue can potentially be caused by SubnetActorManagerFacet.stake function as shown in the following:
```solidity
   function stake() external payable whenNotPaused notKilled {
        ...
        // AUDIT:  dust stakers are allowed
        if (msg.value == 0) {
            revert CollateralIsZero();
        }
        ...
        // AUDIT: genesisValidators are added up here
        if (!s.bootstrapped) {
            LibStaking.depositWithConfirm(msg.sender, msg.value);
            return;
        }
        LibStaking.deposit(msg.sender, msg.value);
    }
```
**Recommendation** - 

This issue can be avoided joining the network demands a certain amount of stake to be paid upfront.

**Fix**:  Client acknowledged that the risk is low at the moment, in addition, this is to be addressed in the future.
