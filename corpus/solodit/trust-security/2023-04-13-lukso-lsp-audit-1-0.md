---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-04-13-lukso-lsp-audit-1-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-04-13T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-04-13-LUKSO%20LSP%20audit.md
tags:
- firm:trust-security
- report:2023-04-13-lukso-lsp-audit
title: TRST-M-1 LSP20 verification library deviates from spec and will accept fail
  values
vuln_class: []
---

# TRST-M-1 LSP20 verification library deviates from spec and will accept fail values

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-04-13-LUKSO LSP audit.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-04-13-LUKSO%20LSP%20audit.md)_

---

**Description:**
The functions `lsp20VerifyCall()` and `lsp20VerifyCallResult()` are called to validate the owner 
accepts some account interaction. The specification states they must return a specific 4 byte 
magic value. 
However, the implementation will accept any byte array that starts with the required magic 
value.
```solidity
    function _verifyCall(address logicVerifier) internal virtual returns (bool verifyAfter) {
        (bool success, bytes memory returnedData) = logicVerifier.call(
            abi.encodeWithSelector(ILSP20.lsp20VerifyCall.selector, msg.sender, msg.value, msg.data)
    );
    if (!success) _revert(false, returnedData);
    if (returnedData.length < 32) revert 
      LSP20InvalidMagicValue(false, returnedData);
        bytes32 magicValue = abi.decode(returnedData, (bytes32));
    if (bytes3(magicValue) != 
      bytes3(ILSP20.lsp20VerifyCall.selector))
        revert LSP20InvalidMagicValue(false, returnedData);
    return bytes1(magicValue[3]) == 0x01 ? true : false;
    }
```
Therefore, implementations of the above functions which intend to signal failure status may 
be accepted by the verification wrapper above.

**Recommended Mitigation:**
Verify that the return data length is 32 bytes (the 4 bytes are extended by the compiler), and 
that all other bytes are zero.


**Team Response:**
Fixed (applied recommendation).

**Mitigation review:**
The code correctly validates only the first four bytes are not zero. Code will still accept data 
length which is greater than 32 bytes, which has been confirmed as a design decision
