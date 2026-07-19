---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-05-23-mozaic-archimedes-1-7
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
title: TRST-M-8 The vault cannot operate with popular non-conforming ERC20 tokens
  due to unsafe transfers
vuln_class: []
---

# TRST-M-8 The vault cannot operate with popular non-conforming ERC20 tokens due to unsafe transfers

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-05-23-Mozaic Archimedes.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md)_

---

**Description:**
In Vault, the admin can deposit and withdraw tokens using the functions below:
```solidity
        ///@notice Withdraw token with specified amount.
        function withdrawToken(address _token, uint256 _amount) external onlyAdmin {
             require(_amount != 0, "ERROR: Invalid amount");
                uint256 _curAmount = IERC20(_token).balanceOf(address(this));
                    require(_curAmount >= _amount, "ERROR: Current balance is too low");
        IERC20(_token).transfer(msg.sender, _amount);
        }
        ///@notice Deposit token with specified amount.
        function depositToken(address _token, uint256 _amount) external onlyAdmin {
                require(isAcceptingToken(_token), "ERROR: Invalid token");
                    require(_amount != 0, "ERROR: Invalid amount");
                        IERC20(_token).transferFrom(msg.sender, address(this), _amount);
        }
```
However, it uses `transfer()`/`transferFrom()` directly, instead of using a safe transfer library. 
There are hundreds of tokens who do not use the standard ERC20 signature and return void. 
Such tokens (USDT, BNB, etc.) would be incompatible with the Vault.

**Recommended mitigation:**
Use the SafeERC20 library. Indeed, it has already been imported to Vault.
```solidity
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
```

**Team response:**
Fixed.

**Mitigation review:**
All transfers have been fixed in Vault. However, StargatePlugin still uses unsafe transfers.
