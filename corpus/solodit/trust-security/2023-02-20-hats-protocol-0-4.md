---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-20-hats-protocol-0-4
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-02-20T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md
tags:
- firm:trust-security
- report:2023-02-20-hats-protocol
title: TRST-H-5 Minority may be able to call safe operations
vuln_class: []
---

# TRST-H-5 Minority may be able to call safe operations

_Section severity (from Solodit section header): High_  
_Audit firm: Trust Security_  
_Source report: [2023-02-20-Hats Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md)_

---

**Description:**
Users can update the HSG's view of signers using reconcileSignerCount()
```solidity
        function reconcileSignerCount() public {
            address[] memory owners = safe.getOwners();
                 uint256 validSignerCount = _countValidSigners(owners);
        // update the signer count accordingly
        signerCount = validSignerCount;
        if (validSignerCount <= targetThreshold && validSignerCount != safe.getThreshold())
             {
        bytes memory data =  abi.encodeWithSignature("changeThreshold(uint256)", validSignerCount);
        bool success = safe.execTransactionFromModule(
        address(safe), // to 0, 
        // value data, // data
        Enum.Operation.Call // operation
        );
        if (!success) {
                   revert FailedExecChangeThreshold();
                }
             }
         }
```
Notice that the safe's registered threshold is only updated if the new **validSignerCount** is 
lower than the **targetThreshold**. Actually, that is not desired behavior, because if signers
have reactivated or have become eligible again, it's possible this condition doesn't hold, and 
the previous threshold could be lower than **targetThreshold**. In this scenario, a small 
minority could still execute TXs when **targetThreshold** signatures are needed

**Recommended mitigation:**
Add an else clause, stating that if the new **validSignerCount > targetThreshold** and 
**safe.getThreshold() < targetThreshold**, the threshold changes to **targetThreshold**.

**Team response:**
Accepted.

**Mitigation review:**
Fixed by restructuring conditions in `reconcileSignerCount()`
