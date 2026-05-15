---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-20-hats-protocol-2-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-02-20T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md
tags:
- firm:trust-security
- report:2023-02-20-hats-protocol
title: TRST-L-3 Fetching of hat status may fail due to lack of input sanitization
vuln_class: []
---

# TRST-L-3 Fetching of hat status may fail due to lack of input sanitization

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-02-20-Hats Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md)_

---

**Description:**
The functions `_isActive()` and `_isEligible()` are used by `balanceOf()` and other functions, so 
they should not ever revert. However, they perform ABI decoding from external inputs.
```solidity
        function _isActive(Hat memory _hat, uint256 _hatId) internal view  returns (bool) {
        bytes memory data = 
             abi.encodeWithSignature("getHatStatus(uint256)", _hatId);
                (bool success, bytes memory returndata) = 
        _hat.toggle.staticcall(data);
        if (success && returndata.length > 0) {
            return abi.decode(returndata, (bool));
                } else {
        return _getHatStatus(_hat);
                }
         }
```
If **toggle** returns invalid return data (whether malicious or by accident), `abi.decode()` would 
revert causing the entire function to revert.

**Recommended Mitigation:**
Wrap the decoding operation for both affected functions in a try/catch statement. Fall back 
to the `_getHatStatus()` result if necessary. Checking that **returndata** size is correct is not 
enough as bool encoding must be 64-bit encoded 0 or 1.

**Team response:**
Accepted.

**Mitigation review:**
Fixed by performing safe decoding of input data, and falling back to the static hat status or 
standing.
