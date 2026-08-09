---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-05-23-mozaic-archimedes-0-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-05-23T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md
tags:
- firm:trust-security
- report:2023-05-23-mozaic-archimedes
title: TRST-H-2 Attacker can freeze deposits and withdrawals indefinitely by submitting
  a bad withdrawal
vuln_class: []
---

# TRST-H-2 Attacker can freeze deposits and withdrawals indefinitely by submitting a bad withdrawal

_Section severity (from Solodit section header): High_  
_Audit firm: Trust Security_  
_Source report: [2023-05-23-Mozaic Archimedes.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md)_

---

**Description:**
Users request to queue a withdrawal using the function below in Vault.
```solidity
        function addWithdrawRequest(uint256 _amountMLP, address _token) external {
            require(isAcceptingToken(_token), "ERROR: Invalid token");
                require(_amountMLP != 0, "ERROR: Invalid amount");
        
        address _withdrawer = msg.sender;
        // Get the pending buffer and staged buffer.
             RequestBuffer storage _pendingBuffer = _requests(false);
             RequestBuffer storage _stagedBuffer = _requests(true);
        // Check if the withdrawer have enough balance to withdraw.
        uint256 _bookedAmountMLP =  _stagedBuffer.withdrawAmountPerUser[_withdrawer] + 
       _pendingBuffer.withdrawAmountPerUser[_withdrawer];
            require(_bookedAmountMLP + _amountMLP <= 
                MozaicLP(mozLP).balanceOf(_withdrawer), "Withdraw amount > amount  MLP");
        …
        emit WithdrawRequestAdded(_withdrawer, _token, chainId, _amountMLP);
        }
```
Notice that the function only validates that the user has a sufficient LP token balance to 
withdraw at the moment of execution. After it is queued up, a user can move their tokens to 
another wallet. Later in `_settleRequests()`, the Vault will attempt to burn user's tokens:
```solidity
                // Burn moazic LP token.
            MozaicLP(mozLP).burn(request.user, _mlpToBurn);
 ```
This would revert and block any other settlements from occurring. Therefore, users can block 
the entire settlement process by requesting a tiny withdrawal amount in every epoch and 
moving funds to another wallet.

**Recommended Mitigation:**
Vault should take custody of user's LP tokens when they request withdrawals. If the entire 
withdrawal cannot be satisfied, it can refund some tokens back to the user.

**Team response:**
Fixed.

**Mitigation Review:**
The Vault now holds custody of withdrawn LP tokens. If it is not able to transfer the desired 
amount of stablecoins, it will transfer the remaining LP tokens back to the user.
