---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-01-08-ninja-yield-farming-v3-1-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-01-08T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-08-Ninja%20Yield%20Farming%20v3.md
tags:
- firm:trust-security
- report:2023-01-08-ninja-yield-farming-v3
title: TRST-M-1 Unsafe transferFrom breaks compatibility with 100s of ERC20 tokens
vuln_class: []
---

# TRST-M-1 Unsafe transferFrom breaks compatibility with 100s of ERC20 tokens

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-01-08-Ninja Yield Farming v3.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-08-Ninja%20Yield%20Farming%20v3.md)_

---

**Description:**
In Ninja vaults, the delegated strategy sends profit tokens to the vault using 
`depositProfitTokenForUsers()`. The vault transfers the tokens in using:
```solidity 
         // Now pull in the tokens (Should have permission)
          // We only want to pull the tokens with accounting
                profitToken.transferFrom(strategy, address(this), _amount);
          emit ProfitReceivedFromStrategy(_amount);

```
The issue is that the code doesn't use the `safeTransferFrom()` utility from SafeERC20. 
Therefore, profitTokens that don't return a bool in `transferFrom()` will cause a revert which 
means they are stuck in the strategy. 
Examples of such tokens are USDT, BNB, among hundreds of other tokens.

**Recommended Mitigation:**
Use `safeTransferFrom()` from SafeERC20.sol

**Team Response:**
Accepted. Excellent find. I can't believe we missed this.
