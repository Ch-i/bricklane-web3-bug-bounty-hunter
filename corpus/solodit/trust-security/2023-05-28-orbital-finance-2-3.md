---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-05-28-orbital-finance-2-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-05-28T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-28-Orbital%20Finance.md
tags:
- firm:trust-security
- report:2023-05-28-orbital-finance
title: TRST-L-4 Owner can steal all funds
vuln_class: []
---

# TRST-L-4 Owner can steal all funds

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-05-28-Orbital Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-28-Orbital%20Finance.md)_

---

**Description:**
The owner can set a new operator using the function below:
```solidity
      function setOperator(address operatorIn) external nonReentrant {
         require(msg.sender == owner() || msg.sender == operator, "only ownop");
      operator = operatorIn;
      }
```
They can also allow an arbitrary, malicious router with the code below:
```solidity
         function allowRouter(address routerAddress, string calldata nameIn, uint256 routerType) external      onlyOwner 
             returns (address routerInfoContractAddress){
                require(!allowedRoutersMap[routerAddress].allowed, "router allowed");
                   require(routerType == 0 || routerType == 1, "must be 0 or 1");
                   allowedRoutersList.push(routerAddress);
            RouterInfo ri = new RouterInfo(owner(), nameIn, routerAddress, 
         routerType);
            allowedRoutersMap[routerAddress] = routerInfo(true, 
            allowedRoutersList.length 
         - 1, 
            address(ri));
         
            return address(ri);
         
         }
```
During trading, routers receive MAX approval.
```solidity
         //make sure router can spend vault's spend token
         //alternate idea: transfer tokens to this contract, trade, transfer back
            uint256 currentAllowance =  IERC20(params.spendToken).allowance(vaultAddress, 
                params.routerAddress);
             if (currentAllowance < params.spendAmt)
         vlt.increaseAllowance(params.spendToken, params.routerAddress, 
            type(uint256).max - currentAllowance);
```
The combination of these permissions allows an owner to drain all deployed vaults, by adding 
a malicious router, taking over as operator and calling the `trade()` function.

**Team response:**
"Removed owner permissions from change operator. Autotrade can now only trade when 
autotradeActive flag is set to true. Added a lockRouters() function to Aux contract. This will 
allow me to keep control while the project is getting started. Later, the routers can be locked 
to prevent any new ones from being added. Added checks at the end of the Trade function to 
verify transaction resulted in balance updates as intended."

**Mitigation review:**
The code changes described above reduce the centralization risks by a significant degree. 
Users are urged to validate that all routers are legitimate after the router list is locked down.
