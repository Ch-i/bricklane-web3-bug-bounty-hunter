---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-20-hats-protocol-2-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-02-20T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md
tags:
- firm:trust-security
- report:2023-02-20-hats-protocol
title: TRST-L-2 Incorrect imageURI is returned for hats in certain cases
vuln_class: []
---

# TRST-L-2 Incorrect imageURI is returned for hats in certain cases

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-02-20-Hats Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md)_

---

**Description:**
Function `getImageURIForHat()` should return the most relevant imageURI for the requested 
hatId. It will iterate backwards from the current level down to level 0, and return an image if 
it exists for that level.
```solidity
            function getImageURIForHat(uint256 _hatId) public view returns (string memory) {
                // check _hatId first to potentially avoid the `getHatLevel` call
                      Hat memory hat = _hats[_hatId];
                        string memory imageURI = hat.imageURI; // save 1 SLOAD
                // if _hatId has an imageURI, we return it
                            if (bytes(imageURI).length > 0) {
                return imageURI;
                }
                // otherwise, we check its branch of admins
                        uint256 level = getHatLevel(_hatId);
                // but first we check if _hatId is a tophat, in which case we fall back to the global image uri
                if (level == 0) return baseImageURI;
                // otherwise, we check each of its admins for a valid imageURI
                     uint256 id;
                // already checked at `level` above, so we start the loop at `level - 1`
                for (uint256 i = level - 1; i > 0;) {
                     id = getAdminAtLevel(_hatId, uint8(i));
                        hat = _hats[id];
                            imageURI = hat.imageURI;
                if (bytes(imageURI).length > 0) {
                      return imageURI;
                 }
                // should not underflow given stopping condition is > 0
                    unchecked {
                         --i;
                    }
             }
                // if none of _hatId's admins has an imageURI of its own, we 
            again fall back to the global image uri
                return baseImageURI;
            }
```
It can be observed that the loop body will not run for level 0. When the loop is finished, the 
code just returns the baseImageURI, which is a Hats-level fallback, rather than top hat level fallback. As a result, the image displayed will not be correct when querying for a level above 
0, when all levels except level 0 have no registered image.

**Recommended Mitigation:**
Before returning the **baseImageURI**, check if level 0 admin has a registered image.

**Team Response:**
Fixed using an additional check.
