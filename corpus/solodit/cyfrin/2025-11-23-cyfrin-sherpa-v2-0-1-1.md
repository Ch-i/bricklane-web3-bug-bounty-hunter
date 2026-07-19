---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-23-cyfrin-sherpa-v2-0-1-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-11-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-23-cyfrin-sherpa-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-23-cyfrin-sherpa-v2-0
title: SherpaUSD does not work with fee-on-transfer tokens
vuln_class: []
---

# SherpaUSD does not work with fee-on-transfer tokens

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-23-cyfrin-sherpa-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-23-cyfrin-sherpa-v2.0.md)_

---

**Description:** The SherpaUSD contract cannot work correctly with fee-on-transfer tokens. An example of such a token is USDT, which is expected to be supported as per comments. Note: Fees are not yet activated on USDT however they can be at any time in the future.

```solidity
        // CRITICAL: SherpaUSD only supports 6-decimal assets (USDC, USDT, etc.)
```

For example:
 - Assume 2% fees are charged by a fee-on-transfer token.
 - Keeper calls function depositToVault with 100e6 as amount.
 - 100 SherpaUSD are minted to the keeper
 - Due to fees charged on transfer, only 98 tokens are received by the contract.
 - This can build up over time and cause late withdrawers to incur a loss as they will be unable to withdraw fully or a partial amount of their tokens.
```solidity
function depositToVault(
    address from,
    uint256 amount
) external nonReentrant onlyKeeper {
    if (amount == 0) revert AmountMustBeGreaterThanZero();

    _mint(keeper, amount);
    depositAmountForEpoch += amount;

    emit DepositToVault(from, amount);

    IERC20(asset).safeTransferFrom(from, address(this), amount);
}
```

**Recommended Mitigation:** Consider adding support for fee-on-transfer tokens. Alternatively consider not supporting such tokens.

**Sherpa:** Fixed on commit [`0b32641`](https://github.com/hedgemonyxyz/sherpa-vault-smartcontracts/commit/0b326416fc7312ee11b279964a947a10b642cc2d)

**Cyfrin:** Verified. Comment changed to explicitly say FOT tokens not supported (including USDT).
