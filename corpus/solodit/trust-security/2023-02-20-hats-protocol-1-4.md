---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-20-hats-protocol-1-4
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-02-20T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md
tags:
- firm:trust-security
- report:2023-02-20-hats-protocol
title: TRST-M-5 Attacker can make a signer gate creation fail
vuln_class: []
---

# TRST-M-5 Attacker can make a signer gate creation fail

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-02-20-Hats Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md)_

---

**Description:** 
DAOs can deploy a HSG using `deployHatsSignerGateAndSafe()` or 
`deployMultiHatsSignerGateAndSafe()`.The parameters are encoded and passed to 
`moduleProxyFactory.deployModule()`:
```solidity
    bytes memory initializeParams = abi.encode(_ownerHatId, _signersHatId, _safe, hatsAddress, _minThreshold, 
    _targetThreshold, _maxSigners, version );
        hsg = moduleProxyFactory.deployModule(hatsSignerGateSingleton, abi.encodeWithSignature("setUp(bytes)", 
    initializeParams), _saltNonce );
```
This function will call `createProxy()`:
```solidity
    proxy = createProxy( masterCopy, keccak256(abi.encodePacked(keccak256(initializer), saltNonce)) );
```
The second parameter is the generated salt, which is created from the initializer and passed 
saltNonce. Finally `createProxy()` will use CREATE2 to create the contract:
```solidity
        function createProxy(address target, bytes32 salt)  internal  returns (address result)
        {
            if (address(target) == address(0)) revert ZeroAddress(target);
            if (address(target).code.length == 0) revert 
        TargetHasNoCode(target);
                bytes memory deployment = abi.encodePacked(
                  hex"602d8060093d393df3363d3d373d3d3d363d73", target, hex"5af43d82803e903d91602b57fd5bf3" );
            // solhint-disable-next-line no-inline-assembly
                assembly {
                     result := create2(0, add(deployment, 0x20), 
        mload(deployment), salt)
              }
                  if (result == address(0)) revert TakenAddress(result);
             }
```
An issue could be that an attacker can frontrun the creation TX with their own creation 
request, with the same parameters. This would create the exact address created by the 
CREATE2 call, since the parameters and therefore the final salt will be the same. When the 
victim's transaction would be executed, the address is non-empty so the EVM would reject 
its creation. This would result in a bad UX for a user, who thinks the creation did not 
succeed. The result contract would still be usable, but would be hard to track as it was 
created in another TX.

**Recommended Mitigation:**
Use an ever-increasing nonce counter to guarantee unique contract addresses.

**Team response:**
Accepted.
