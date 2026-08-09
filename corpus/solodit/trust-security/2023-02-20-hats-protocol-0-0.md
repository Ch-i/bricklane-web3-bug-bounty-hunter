---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-20-hats-protocol-0-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-02-20T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md
tags:
- firm:trust-security
- report:2023-02-20-hats-protocol
title: TRST-H-1 More than one hat of the same hatId can be assigned to a user
vuln_class: []
---

# TRST-H-1 More than one hat of the same hatId can be assigned to a user

_Section severity (from Solodit section header): High_  
_Audit firm: Trust Security_  
_Source report: [2023-02-20-Hats Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md)_

---

**Description:**
Hats are minted internally using `_mintHat()`.
```solidity
        /// @notice Internal call to mint a Hat token to a wearer
        /// @dev Unsafe if called when `_wearer` has a non-zero balance of `_hatId`
        /// @param _wearer The wearer of the Hat and the recipient of the  newly minted token
        /// @param _hatId The id of the Hat to mint
        function _mintHat(address _wearer, uint256 _hatId) internal {
            unchecked {
        // should not overflow since `mintHat` enforces max balance of 1
            _balanceOf[_wearer][_hatId] = 1;
        // increment Hat supply counter
        // should not overflow given AllHatsWorn check in `mintHat` ++_hats[_hatId].supply;
        }
        emit TransferSingle(msg.sender, address(0), _wearer, _hatId, 1);
        }
```
As documentation states, it is unsafe if **_wearer** already has the **hatId**. However, this could 
easily be the case when called from `mintHat()`. 
```solidity
        function mintHat(uint256 _hatId, address _wearer) public returns (bool) {
        Hat memory hat = _hats[_hatId];
            if (hat.maxSupply == 0) revert HatDoesNotExist(_hatId);
        // only the wearer of a hat's admin Hat can mint it
             _checkAdmin(_hatId);
            if (hat.supply >= hat.maxSupply) {
                 revert AllHatsWorn(_hatId);
                     }
        if (isWearerOfHat(_wearer, _hatId)) {
                revert AlreadyWearingHat(_wearer, _hatId);
                      }
        _mintHat(_wearer, _hatId);
             return true;
                  }
```
The function validates **_wearer** doesn't currently wear the hat, but its balance could still be 
over 0, if the hat is currently toggled off or the wearer is not eligible.
The impact is that the hat supply is forever spent, while nobody actually received the hat. 
This could be used maliciously or occur by accident. When the hat is immutable, the max 
supply can never be corrected for this leak. It could be used to guarantee no additional, 
unfriendly hats can be minted to maintain permanent power.

**Recommended Mitigation:**
Instead of checking if user currently wears the hat, check if its balance is over 0.


**Team response:**
Accepted.

**Mitigation review:**
Fixed by checking the static hat balance of wearer.
