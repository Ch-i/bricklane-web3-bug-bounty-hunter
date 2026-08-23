---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-01-08-ninja-yield-farming-v3-2-4
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-01-08T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-08-Ninja%20Yield%20Farming%20v3.md
tags:
- firm:trust-security
- report:2023-01-08-ninja-yield-farming-v3
title: TRST-L-5 Strategy deployer has privileges intended only for multisig addresses.
vuln_class: []
---

# TRST-L-5 Strategy deployer has privileges intended only for multisig addresses.

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-01-08-Ninja Yield Farming v3.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-08-Ninja%20Yield%20Farming%20v3.md)_

---

**Description:** 
When V3 Strategy is initialized, different roles are given to privileged addresses:
```solidity
         for (uint256 i = 0; i < _strategists.length; i++) {
            _grantRole(STRATEGIST, _strategists[i]);
               }
               _grantRole(DEFAULT_ADMIN_ROLE, msg.sender); // @audit - Is this a security risk? Default admin roles is REALLY powerful! Consider removing
            _grantRole(DEFAULT_ADMIN_ROLE, _multisigRoles[0]);
         _grantRole(ADMIN, _multisigRoles[1]);
         _grantRole(GUARDIAN, _multisigRoles[2]);
 ```
As the previous @audit note says, it is really important to not permit msg.sender to be 
**DEFAULT_ADMIN_ROLE**. In fact, this role gives arbitrary power to the EOA, to remove the 
multisig, to assign itself any of the roles, and so on. In a way, it makes the multisig be just for 
show. Since Strategy is effectively responsible to hold the vault's funds, and can be 
upgraded, this represents a worrying rug pull potential.

**Team response:**
Reduced deployer access to GUARDIAN means they do not have any upgrade capability. 
They can pause contracts and perform STRATEGIST/KEEPER roles. We have also added a 
revokeDeployer function which GUARDIANS and above can use to remove the deployers 
access.
