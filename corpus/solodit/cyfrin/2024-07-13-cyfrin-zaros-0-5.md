---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-13-cyfrin-zaros-0-5
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-07-13T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md
tags:
- firm:cyfrin
- report:2024-07-13-cyfrin-zaros
title: '`TradingAccountBranch::depositMargin` attempts to transfer greater amount
  than user deposited for tokens with less than 18 decimals'
vuln_class: []
---

# `TradingAccountBranch::depositMargin` attempts to transfer greater amount than user deposited for tokens with less than 18 decimals

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-13-cyfrin.zaros.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md)_

---

**Description:** For collateral tokens with less than 18 decimals, `TradingAccountBranch::depositMargin` attempts to transfer a greater amount of tokens than what the user is actually depositing as:
* input `amount` is converted into `ud60x18Amount` via `MarginCollateralConfiguration::convertTokenAmountToUd60x18` which [scales up `amount` to 18 decimals](https://github.com/zaros-labs/zaros-core-audit/blob/de09d030c780942b70f1bebcb2d245214144acd2/src/perpetuals/leaves/MarginCollateralConfiguration.sol#L46-L50)
* the `safeTransferFrom` call is passed `ud60x18Amount::intoUint256` which converts that scaled up input amount back to `uint256`

```solidity
function depositMargin(uint128 tradingAccountId, address collateralType, uint256 amount) public virtual {
    // load margin collateral config for this collateral type
    MarginCollateralConfiguration.Data storage marginCollateralConfiguration =
        MarginCollateralConfiguration.load(collateralType);

    // @audit convert uint256 -> UD60x18; scales input amount to 18 decimals
    UD60x18 ud60x18Amount = marginCollateralConfiguration.convertTokenAmountToUd60x18(amount);

    // *snip* //

    // @audit fetch tokens from the user; using the ud60x18Amount which has been
    // scaled up to 18 decimals. Will attempt to transfer more tokens than
    // user actually depositing
    IERC20(collateralType).safeTransferFrom(msg.sender, address(this), ud60x18Amount.intoUint256());
```

**Impact:** For collateral tokens with less than 18 decimals, `TradingAccountBranch::depositMargin` will attempt to transfer more tokens than the user is actually depositing. If the user has not approved the greater amount (or infinite approval) the transaction will revert; similarly if the user does not have sufficient funds it will also revert. If the user has sufficient funds and has granted the approval the user's tokens will be stolen by the protocol.


**Recommended Mitigation:** The `safeTransferFrom` should use `amount` instead of `ud60x18Amount`.

```diff
- IERC20(collateralType).safeTransferFrom(msg.sender, address(this), ud60x18Amount.intoUint256());
+ IERC20(collateralType).safeTransferFrom(msg.sender, address(this), amount);
```

**Zaros:** Fixed in commit [3fe9c0a](https://github.com/zaros-labs/zaros-core/commit/3fe9c0a21394cbbb0fc9999dfd534e2b723cc071#diff-b7968970769299fcdbfb6ef6a99fb78342b70e422a56416e5d9c107e5a009fc3R274).

**Cyfrin:** Verified.
