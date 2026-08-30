---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-20-hats-protocol-1-5
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-02-20T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md
tags:
- firm:trust-security
- report:2023-02-20-hats-protocol
title: TRST-M-6 Signers can backdoor the safe to execute any transaction in the future
  without consensus
vuln_class: []
---

# TRST-M-6 Signers can backdoor the safe to execute any transaction in the future without consensus

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-02-20-Hats Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md)_

---

**Description:** 
The function `checkAfterExecution()` is called by the safe after signer's request TX was 
executed (and authorized). It mainly checks that the linkage between the safe and the HSG 
has not been compromised.
```solidity
        function checkAfterExecution(bytes32, bool) external override {
            if (abi.decode(StorageAccessible(address(safe)).getStorageAt(uint256(GUARD_STORAGE_SLOT), 1), (address))
                    != address(this)) 
                    {
                revert CannotDisableThisGuard(address(this));
            }
            if (!IAvatar(address(safe)).isModuleEnabled(address(this))) {
                    revert CannotDisableProtectedModules(address(this));
            }
            if (safe.getThreshold() != _correctThreshold()) {
                     revert SignersCannotChangeThreshold();
            }
            // leave checked to catch underflows triggered by re-erntry
        attempts
            --guardEntries;
        }
```
However, it is missing a check that no new modules have been introduced to the safe. When 
modules execute TXs on a Gnosis safe, the guard safety callbacks do not get called. As a 
result, any new module introduced is free to execute whatever it wishes on the safe. It 
constitutes a serious backdoor threat and undermines the HSG security model.

**Recommended Mitigation:**
Check that no new modules have been introduced to the safe, using the 
`getModulesPaginated()` utility.

**Team response:**
Accepted; added a method for HSG owner to add modules, and an enabled modules counter 
to check against in `checkAfterTransaction()`

**Mitigation review:**
Fix is not bulletproof. A malicious transaction can remove an existing module and replace it 
with their own malicious module. In addition to a length check on the modules array, it is 
necessary to do a full comparison before and after the TX execution.
