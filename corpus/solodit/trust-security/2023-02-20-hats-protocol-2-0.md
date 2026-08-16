---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-20-hats-protocol-2-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-02-20T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md
tags:
- firm:trust-security
- report:2023-02-20-hats-protocol
title: TRST-L-1 createHat does not detect MAX_LEVEL admin correctly
vuln_class: []
---

# TRST-L-1 createHat does not detect MAX_LEVEL admin correctly

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-02-20-Hats Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md)_

---

**Description:**
In `createHat()`, the contract checks user is not minting hats for the lowest hat tier:
```solidity
        function createHat( uint256 _admin, string memory _details, uint32 _maxSupply, address _eligibility,
            address _toggle, bool _mutable,  string memory _imageURI)       
                 public returns (uint256 newHatId) {
        if (uint8(_admin) > 0) {
                    revert MaxLevelsReached();
                 }
             ….
        }
```

The issue is that it does not check for max level correctly, as it looks only at the lowest 8 bits. 
Each level is composed of 16 bits, so ID xx00 would pass this check. 
Fortunately, although the check is passed, the function will revert later. The call to 
`getNextId(_admin)` will return 0 for max-level admin, and _checkAdmin(0) is guaranteed to 
fail. However, the check should still be fixed as it is not exploitable only by chance.

**Recommended Mitigation:**
Change the conversion to uint16.

**Team Response:**
Accepted.

**Mitigation review:**
Fixed.
