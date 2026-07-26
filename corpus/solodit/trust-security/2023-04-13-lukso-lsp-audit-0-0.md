---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-04-13-lukso-lsp-audit-0-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-04-13T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-04-13-LUKSO%20LSP%20audit.md
tags:
- firm:trust-security
- report:2023-04-13-lukso-lsp-audit
title: TRST-H-1 Reentrancy protection can likely be bypassed
vuln_class: []
---

# TRST-H-1 Reentrancy protection can likely be bypassed

_Section severity (from Solodit section header): High_  
_Audit firm: Trust Security_  
_Source report: [2023-04-13-LUKSO LSP audit.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-04-13-LUKSO%20LSP%20audit.md)_

---

**Description:**
The KeyManager offers reentrancy protection for interactions with the associated account. 
Through the LSP20 callbacks or through the `execute()` calls, it will call `_nonReentrantBefore()`
before execution, and `_nonReentrantAfter()` post-execution. The latter will always reset the 
flag signaling entry.
```solidity
    function _nonReentrantAfter() internal virtual {
    // By storing the original value once again, a refund is triggered 
             (see // https://eips.ethereum.org/EIPS/eip-2200)
        _reentrancyStatus = false;
     }
```
An attacker can abuse it to reenter provided that there exists some third-party contract with 
REENTRANCY_PERMISSION that performs some interaction with the contract. The attacker 
would trigger the third-party code path, which will clear the reentrancy status, and enable 
attacker to reenter. This could potentially be chained several times. Breaking the reentrancy 
assumption would make code that assumes such flows to be impossible to now be vulnerable.

**Recommended Mitigation:**
In `_nonReentrantAfter()`, the flag should be returned to the original value before reentry, 
rather than always setting it to false.

**Team response:**
Applied a fix different than recommendation.

**Mitigiation review:**
All code paths will now leave the **_reentrancyStatus** on when the current call is not the initial 
call to the KeyManager.
