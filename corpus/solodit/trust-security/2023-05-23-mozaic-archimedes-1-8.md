---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-05-23-mozaic-archimedes-1-8
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-05-23T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md
tags:
- firm:trust-security
- report:2023-05-23-mozaic-archimedes
title: TRST-M-9 Vault does not have a way to withdraw native tokens
vuln_class: []
---

# TRST-M-9 Vault does not have a way to withdraw native tokens

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-05-23-Mozaic Archimedes.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md)_

---

**Description:**
The Vault sets the LayerZero fee refund address to itself:
```solidity
        /// @notice Report snapshot of the vault to the controller.
        function reportSnapshot() public onlyBridge {
                 MozBridge.Snapshot memory _snapshot = _takeSnapshot();
             MozBridge(mozBridge).reportSnapshot(_snapshot, 
          payable(address(this)));
        }
```
However, there is no function to withdraw those funds, making them forever stuck in the vault 
only available for paying for future transactions.

**Recommended mitigation:**
Add a native token withdrawal function.

**Team response:**
Fixed.

**Mitigation review:**
The fix includes a new `withdraw()` function. Its intention is to vacate any ETH stored in the 
controller and vaults.

```solidity
        function withdraw() public {
        // get the amount of Ether stored in this contract
            uint amount = address(this).balance;
        // send all Ether to owner
        // Owner can receive Ether since the address of owner is payable
            (bool success, ) = treasury.call{value: amount}("");
                 require(success, "Controller: Failed to send Ether");
         }
```
In fact, attackers can simply call `withdraw()` to make messaging fail due to lack of native
tokens. This could be repeated in every block to make the system unusable.
