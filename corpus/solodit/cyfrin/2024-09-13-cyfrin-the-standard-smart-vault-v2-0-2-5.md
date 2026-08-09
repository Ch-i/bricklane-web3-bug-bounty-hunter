---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-09-13-cyfrin-the-standard-smart-vault-v2-0-2-5
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-09-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md
tags:
- firm:cyfrin
- report:2024-09-13-cyfrin-the-standard-smart-vault-v2-0
title: Liquidations could be blocked by reverting ERC-20 transfers
vuln_class: []
---

# Liquidations could be blocked by reverting ERC-20 transfers

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md)_

---

**Description:** When liquidations are performed via `SmartVaultV4::liquidate`, ERC-20 collateral tokens are handled within a loop:

```solidity
function liquidate() external onlyVaultManager {
    /* snip: validation, state updates & native liquidation
    ITokenManager.Token[] memory tokens = ITokenManager(ISmartVaultManagerV3(manager).tokenManager()).getAcceptedTokens();
    for (uint256 i = 0; i < tokens.length; i++) {
        if (tokens[i].symbol != NATIVE) liquidateERC20(IERC20(tokens[i].addr));
    }
}
```

If the contract balance of a given ERC-20 is non-zero, it will proceed to perform a transfer to the protocol address, as show below:

```solidity
function liquidateERC20(IERC20 _token) private {
    if (_token.balanceOf(address(this)) != 0) _token.safeTransfer(ISmartVaultManagerV3(manager).protocol(), _token.balanceOf(address(this)));
}
```

However, if any of these transfers revert, the whole call will revert and liquidation will be blocked. Analysis of the collateral tokens currently intended to be supported failed to identify any immediate risks, although it is prescient to note the following:
- `GMX` includes rewards distribution logic on transfers (that, however unlikely, could potentially revert).
- `WETH` and `ARB` are Transparent Upgradeable proxies.
- `WBTC`, `LINK`, `PAXG`, and `SUSHI` are Beacon proxies.
- `RDNT` is a LayerZero bridge token.

**Impact:** Liquidations for a given Smart Vault will be blocked if `GMX` collateral transfers revert. If any other collateral tokens are upgraded to introduce novel transfer logic, they could also make Smart Vaults susceptible to this issue. If an attacker can force a single collateral token transfer to revert, they can avoid being liquidated.

**Recommended Mitigation:** Consider separate handling of each ERC-20 transfer with `try/catch` to avoid blocked liquidations.

**The Standard DAO:** Fixed by commit [`efda8d2`](https://github.com/the-standard/smart-vault/commit/efda8d2de7cb4406598d50099f52fc1275769c0a).

**Cyfrin:** Verified, liquidation will no longer revert if a single transfer fails. Direct use of `ERC20::transfer` instead of `SafeERC20::safeTransfer` appears to be okay because:
- The Smart Vault will always be calling a contract with code when looping through the accepted tokens
- The current list of accepted collateral tokens all return `true` or revert on failed transfer.
