---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-05-23-mozaic-archimedes-2-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-05-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md
tags:
- firm:trust-security
- report:2023-05-23-mozaic-archimedes
title: TRST-L-2 XMozToken permits transfers from non-whitelisted addresses
vuln_class: []
---

# TRST-L-2 XMozToken permits transfers from non-whitelisted addresses

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-05-23-Mozaic Archimedes.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md)_

---

**Description:**
The XMozToken is documented to forbid transfers except from whitelisted addresses or mints.
```solidity
        /**
        * @dev Hook override to forbid transfers except from whitelisted 
        addresses and minting
        */
        function _beforeTokenTransfer(address from, address to, uint256 
        /*amount*/) internal view override {
                require(from == address(0) || _transferWhitelist.contains(from) 
                  || _transferWhitelist.contains(to), "transfer: not allowed");
                 }
```
However, as can be seen, non-whitelisted users can still transfer tokens, so long as it is to 
whitelisted destinations. 

**Recommended Mitigation:**
Remove the additional check in `_beforeTokenTransfer()`, or update the documentation 
accordingly.

**Team Response:**
Fixed.

**Mitigation review:**
The check was changed as seen below:
```solidity
        function _beforeTokenTransfer(address from, address to, uint256 
        /*amount*/) internal view override {
              require(from == address(0) || to == address(0) || from == owner() 
                 || isTransferWhitelisted(from), "transfer: not allowed");
             }
```
The original issue is fixed, however the **to == address(0)** check introduced a new major issue. 
It is used to allow the burning of tokens for the MozStaking contract. As a side-effect, it allows 
users to bridge the XMoz token (which is an OFTv2 token behind the covers). A user can bypass 
the transfer whitelist by bridging the asset and specifying any recipient.
