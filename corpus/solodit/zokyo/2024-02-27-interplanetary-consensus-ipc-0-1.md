---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-02-27-interplanetary-consensus-ipc-0-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-02-27T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md
tags:
- firm:zokyo
- report:2024-02-27-interplanetary-consensus-ipc
title: Arbitrary amount can be withdrawn (stolen)
vuln_class: []
---

# Arbitrary amount can be withdrawn (stolen)

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2024-02-27-InterPlanetary Consensus (IPC).md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md)_

---

**Severity**: Critical

**Status**: Resolved

GatewayManagerFacet.sol - A vulnerability is identified in the `releaseRewardForRelayer` function. The issue allows for arbitrary amount inputs without proper validation, potentially leading to unauthorized fund drainage from the Gateway.
```solidity
   function releaseRewardForRelayer(uint256 amount) external nonReentrant {
        if (amount == 0) {
            revert CannotReleaseZero();
        }

        (bool registered, Subnet storage subnet) = LibGateway.getSubnet(msg.sender);
        if (!registered) {
            revert NotRegisteredSubnet();
        }

        payable(subnet.id.getActor()).sendValue(amount);
    }
```
The `releaseRewardForRelayer` function does not adequately validate the input amount, allowing arbitrary values to be specified. Given that custom subnets are allowed in the project, this presents an opportunity for malicious actors to drain funds from the Gateway by providing arbitrary and unauthorized amount values.

**Recommendation** - 

Validate Amount Input: Implement robust validation checks on the amount parameter to ensure that it is within acceptable and authorized limits.
