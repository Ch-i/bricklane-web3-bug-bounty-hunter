---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-01-08-ninja-yield-farming-v3-2-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-01-08T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-08-Ninja%20Yield%20Farming%20v3.md
tags:
- firm:trust-security
- report:2023-01-08-ninja-yield-farming-v3
title: TRST-L-1 when using fee-on-transfer tokens in VaultV3, capacity is limited
  below underlyingCap
vuln_class: []
---

# TRST-L-1 when using fee-on-transfer tokens in VaultV3, capacity is limited below underlyingCap

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-01-08-Ninja Yield Farming v3.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-08-Ninja%20Yield%20Farming%20v3.md)_

---

**Description:**
Vault V3 documentation states it accounts properly for fee-on-transfer tokens. It calculates 
actual transferred amount as below:
```solidity
      uint256 _pool = balance();
           if (_pool + _amount > underlyingCap) {
      revert NYProfitTakingVault__UnderlyingCapReached(underlyingCap);
            }
      uint256 _before = underlying.balanceOf(address(this));
            underlying.safeTransferFrom(msg.sender, address(this), _amount);
               uint256 _after = underlying.balanceOf(address(this));
                   _amount = _after - _before;
```
A small issue is that underlyingCap is compared to the _amount before correction for actual 
transferred amount. Therefore, it cannot actually be reached, and limits the maximum 
capacity of the vault to underlyingCap minus a factor of the fee %.

**Recommended Mitigation:**
Move the underlyingCap check to below the effective _amount calculation

**Team Response:**
Accepted and updated.
