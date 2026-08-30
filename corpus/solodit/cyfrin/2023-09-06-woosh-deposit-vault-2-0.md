---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-06-woosh-deposit-vault-2-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-09-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-06-Woosh%20Deposit%20Vault.md
tags:
- firm:cyfrin
- report:2023-09-06-woosh-deposit-vault
title: Nonstandard usage of nonce
vuln_class: []
---

# Nonstandard usage of nonce

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-06-Woosh Deposit Vault.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-06-Woosh%20Deposit%20Vault.md)_

---

**Severity:** Informational

**Description:** The protocol implemented two withdraw functions `withdrawDeposit()` and `withdraw()`.
While the function `withdrawDeposit()` is designed to be used by the depositor themselves, the function `withdraw()` is designed to be used by anyone who has a signature from the depositor.
The function `withdraw()` has a parameter `nonce` but the usage of this param is not aligned with the general meaning of nonce.
```solidity
DepositVault.sol
59:     function withdraw(uint256 amount, uint256 nonce, bytes memory signature, address payable recipient) public {
60:         require(nonce < deposits.length, "Invalid deposit index");
61:         Deposit storage depositToWithdraw = deposits[nonce];//@audit-info non aligned with common understanding of nonce
62:         bytes32 withdrawalHash = getWithdrawalHash(Withdrawal(amount, nonce));
63:         address signer = withdrawalHash.recover(signature);
64:         require(signer == depositToWithdraw.depositor, "Invalid signature");
65:         require(!usedWithdrawalHashes[withdrawalHash], "Withdrawal has already been executed");
66:         require(amount == depositToWithdraw.amount, "Withdrawal amount must match deposit amount");
67:
68:         usedWithdrawalHashes[withdrawalHash] = true;
69:         depositToWithdraw.amount = 0;
70:
71:         if(depositToWithdraw.tokenAddress == address(0)){
72:             recipient.transfer(amount);
73:         } else {
74:             IERC20 token = IERC20(depositToWithdraw.tokenAddress);
75:             token.safeTransfer(recipient, amount);
76:         }
77:
78:         emit WithdrawalMade(recipient, amount);
79:     }
```
In common usage, nonce is used to track the latest transaction from the EOA and generally it is increased on the user's transaction. It can be effectively used to invalidate the previous signature by the signer.
But looking at the current implementation, the parameter `nonce` is merely used as an index to refer the `deposit` at a specific index.

This is a bad naming and can confuse the users.

**Recommended Mitigation:** If the protocol intended to provide a kind of invalidation mechanism using the nonce, there should be a separate mapping that stores the nonce for each user. The current nonce can be used to generate a signature and a depositor should be able to increase the nonce to invalidate the previous signatures. Also the nonce would need to be increased on every successful call to `withdraw()` to prevent replay attack.
Please note that with this remediation, the mapping `usedWithdrawalHashes` can be removed completely because the hash will be always decided using the latest nonce and the nonce will be invalidated automatically (because it increases on successful call).

If this is not what the protocol intended, the parameter nonce can be renamed to `depositIndex` as implemented in the function `withdrawDeposit()`.

**Client:**
Fixed in commit [b21d23e](https://github.com/HyperGood/woosh-contracts/commit/b21d23e661b0f25f0e757dc00ee90e4464730b1b).

**Cyfrin:** Verified.
