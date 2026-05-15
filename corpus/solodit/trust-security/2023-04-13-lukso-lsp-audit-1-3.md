---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-04-13-lukso-lsp-audit-1-3
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-04-13T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-04-13-LUKSO%20LSP%20audit.md
tags:
- firm:trust-security
- report:2023-04-13-lukso-lsp-audit
title: TRST-M-4 Incorrect decoding of universalReceiver() call
vuln_class: []
---

# TRST-M-4 Incorrect decoding of universalReceiver() call

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-04-13-LUKSO LSP audit.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-04-13-LUKSO%20LSP%20audit.md)_

---

**Description:**
Some contracts use the utility below to interact with the registered universal receiver 
delegate.
```solidity
    function callUniversalReceiverWithCallerInfos(address universalReceiverDelegate,
        bytes32 typeId, bytes calldata receivedData, address msgSender, uint256 msgValue) internal            returns (bytes memory) {
    bytes memory callData = abi.encodePacked(
           abi.encodeWithSelector(
ILSP1UniversalReceiver.universalReceiver.selector, typeId,receivedData ),
    msgSender,
       msgValue
    );
    (bool success, bytes memory result) = 
        universalReceiverDelegate.call(callData);
    Address.verifyCallResult(success, result, "Call to universalReceiver failed");
          return result.length != 0 ? abi.decode(result, (bytes)) : result;
        }
```
The `universalReceiver()` function has to return a **bytes** type.
```solidity
      function universalReceiver(bytes32 typeId, bytes memory
       /* data */
      )   public payable virtual returns (bytes memory result) {
```
  However, the wrapper above will only decode the low-level call into a **bytes** type when **result**
in non-zero. In fact, when **result** is zero the delegate has returned invalid output (no 
**returndata**). The callee will confuse the response with a valid zero-bytes return value and will 
presumably finish execution.

**Recommended mitigation:**
When the **result** length is zero, revert the transaction.

**Team response:**
It was decided by design to allow empty non-conforming bytes.
