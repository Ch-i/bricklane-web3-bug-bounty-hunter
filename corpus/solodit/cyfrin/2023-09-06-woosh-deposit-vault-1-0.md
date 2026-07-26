---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-06-woosh-deposit-vault-1-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-09-06T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-06-Woosh%20Deposit%20Vault.md
tags:
- firm:cyfrin
- report:2023-09-06-woosh-deposit-vault
title: The deposit function is not following CEI pattern
vuln_class: []
---

# The deposit function is not following CEI pattern

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-06-Woosh Deposit Vault.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-06-Woosh%20Deposit%20Vault.md)_

---

**Severity:** Low

**Description:** The protocol implemented a function `deposit()` to allow users to deposit.
```solidity
DepositVault.sol
37:     function deposit(uint256 amount, address tokenAddress) public payable {
38:         require(amount > 0 || msg.value > 0, "Deposit amount must be greater than 0");
39:         if(msg.value > 0) {
40:             require(tokenAddress == address(0), "Token address must be 0x0 for ETH deposits");
41:             uint256 depositIndex = deposits.length;
42:             deposits.push(Deposit(payable(msg.sender), msg.value, tokenAddress));
43:             emit DepositMade(msg.sender, depositIndex, msg.value, tokenAddress);
44:         } else {
45:             require(tokenAddress != address(0), "Token address must not be 0x0 for token deposits");
46:             IERC20 token = IERC20(tokenAddress);
47:             token.safeTransferFrom(msg.sender, address(this), amount);//@audit-issue against CEI pattern
48:             uint256 depositIndex = deposits.length;
49:             deposits.push(Deposit(payable(msg.sender), amount, tokenAddress));
50:             emit DepositMade(msg.sender, depositIndex, amount, tokenAddress);
51:
52:         }
53:     }
```
Looking at the line L47, we can see that the token transfer happens before updating the accounting state of the protocol against the CEI pattern.
Because the protocol intends to support all ERC20 tokens, the tokens with hooks (e.g. ERC777) can be exploited for reentrancy.
Although we can not verify an exploit that causes explicit loss due to this, it is still highly recommended to follow CEI pattern to prevent possible reentrancy attack.

**Recommended Mitigation:** Handle token transfers after updating the `deposits` state.

**Protocol:**
Fixed in commit [7726ae7](https://github.com/HyperGood/woosh-contracts/commit/7726ae72118cfdf91ceb9129e36662f69f4d42de).

**Cyfrin:** We note that the protocol still does not follow CEI pattern in the final commit [b21d23e](https://github.com/HyperGood/woosh-contracts/commit/b21d23e661b0f25f0e757dc00ee90e4464730b1b).
But we also acknowledge that the fix in [405fa78](https://github.com/HyperGood/woosh-contracts/commit/405fa78a2c0cf8b8ab8943484cb95b5c8807cbfb) to support non-standard ERC20 tokens makes it impossible to follow CEI pattern.
For the current implementation, we verified that there is no reentrancy attack vector due to this issue. If the protocol intends any upgrades in the future related to the `deposits` state, we recommend using [OpenZeppelin's ReentrancyGuard](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/8a0b7bed82d6b8053872c3fd40703efd58f5699d/contracts/security/ReentrancyGuard.sol#L22) to prevent possible reentrancy attack.
Please note that the lack of CEI pattern will still be problematic in the sense of [Read-only reentrancy](https://officercia.mirror.xyz/DBzFiDuxmDOTQEbfXhvLdK0DXVpKu1Nkurk0Cqk3QKc) if the states `deposits` are going to be utilized for any other purposes.
