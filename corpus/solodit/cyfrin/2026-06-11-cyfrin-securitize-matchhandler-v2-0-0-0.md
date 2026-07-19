---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-11-cyfrin-securitize-matchhandler-v2-0-0-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-06-11T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-11-cyfrin-securitize-matchHandler-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-11-cyfrin-securitize-matchhandler-v2-0
title: '`MatchHandler::matchOrder` has no replay protection, allowing duplicate settlement'
vuln_class: []
---

# `MatchHandler::matchOrder` has no replay protection, allowing duplicate settlement

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-11-cyfrin-securitize-matchHandler-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-11-cyfrin-securitize-matchHandler-v2.0.md)_

---

**Description:** `MatchHandler::matchOrder` receives no unique order identifier and stores no consumed-order state. Each authorized call independently executes all transfers, so an operator retry or duplicate queue delivery settles the same off-chain match again whenever both parties retain sufficient balances and aggregate allowances.

```solidity
// contracts/ats/MatchHandler.sol:130
function matchOrder(...) external override whenNotPaused onlyRole(OPERATOR_ROLE) {
    ...
    _updateBuyerInRegistry(IDSToken(dsToken), buyer);
    IDSToken(dsToken).transferFrom(seller, buyer.wallet, dsTokenAmount);
    IERC20(stableCoin).safeTransferFrom(buyer.wallet, seller, sellerPayment);
    IERC20(stableCoin).safeTransferFrom(buyer.wallet, _getStorage().custodialWallet, totalFee);
    // @audit No order ID is marked consumed before or after settlement.
}
```

The registry update is idempotent for a consistent wallet and investor ID, so it does not prevent the repeated value transfers.

**Impact:** A duplicated operator submission can transfer the seller's DS Tokens and the buyer's stablecoin twice, and charge protocol fees twice, exceeding both users' authorized off-chain order amounts. It is noteworthy that this condition is limited to remaining balances and allowances, and only a trusted `OPERATOR_ROLE` can submit the duplicate.

**Proof of Concept:** Add the following test:

```solidity
    function test_POC_DuplicateMatchSettlesTwice() public {
        dsToken.mint(seller, DS_AMOUNT);
        vm.prank(seller);
        dsToken.approve(address(handler), DS_AMOUNT * 2);

        usdc.mint(buyer, USDC_AMOUNT + BUYER_FEE);
        vm.prank(buyer);
        usdc.approve(address(handler), (USDC_AMOUNT + BUYER_FEE) * 2);

        _matchOrder();
        _matchOrder();

        assertEq(dsToken.balanceOf(buyer), DS_AMOUNT * 2, "buyer receives the order twice");
        assertEq(usdc.balanceOf(seller), (USDC_AMOUNT - SELLER_FEE) * 2, "seller is paid twice");
        assertEq(usdc.balanceOf(custodial), (SELLER_FEE + BUYER_FEE) * 2, "fees are charged twice");
        assertEq(usdc.balanceOf(buyer), 0, "buyer pays for two settlements");
    }

```

**Recommended Mitigation:** Consider adding a unique order or match ID to `matchOrder`, mark it consumed before external calls, and revert if it was already consumed.

```solidity
if (settled[matchId]) revert MatchAlreadySettled(matchId);
settled[matchId] = true;
```

The off-chain engine should derive `matchId` deterministically from its canonical match record so retries remain idempotent.

**Securitize:** Fixed in commit [`8ab63ad4`](https://github.com/securitize-io/bc-ats-sc/commit/8ab63ad46ac74250157b94f7e0f79f4ae9206dab)

**Cyfrin:** Verified.
