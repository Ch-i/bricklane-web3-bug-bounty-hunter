---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-11-cyfrin-securitize-matchhandler-v2-0-0-1
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
title: '`MatchHandler::matchOrder` allows same seller and buyer'
vuln_class: []
---

# `MatchHandler::matchOrder` allows same seller and buyer

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-11-cyfrin-securitize-matchHandler-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-11-cyfrin-securitize-matchHandler-v2.0.md)_

---

**Description:** The audit scope states the following

> Input validation rejects: zero addresses, zero amounts, sellerFee > stableCoinAmount , empty buyer.blockchainId , and seller == buyer.wallet. All reverts use typed custom errors from IMatchHandlerErrors.

`MatchHandler::matchOrder` does not enforce the requirement that `seller != buyer.wallet`.

```solidity
// contracts/ats/MatchHandler.sol:130
function matchOrder(...) external override whenNotPaused onlyRole(OPERATOR_ROLE) {
    if (dsToken == address(0) || stableCoin == address(0) || seller == address(0)) revert ZeroAddress();
    if (buyer.wallet == address(0)) revert ZeroAddress();
    // @audit Missing: if (seller == buyer.wallet) revert InvalidCounterparties();
    ...
}
```

When both addresses are equal, the DS Token and seller-payment transfers are self-transfers and have no net economic effect. The combined fee still leaves the trader for the custodial wallet, and a normal `Match` event is emitted.

**Impact:** A malformed off-chain match is recorded on-chain as genuine trading volume even though no assets change counterparties, while the user is charged `sellerFee + buyerFee`. It is noted however that exploitation requires an erroneous or compromised trusted operator.

**Proof of Concept:** Run the following test

```solidity
    function test_POC_SelfMatchProducesFeeOnlySettlement() public {
        address trader = makeAddr("trader");
        uint256 traderFunds = USDC_AMOUNT + BUYER_FEE;

        dsToken.mint(trader, DS_AMOUNT);
        vm.prank(trader);
        dsToken.approve(address(handler), DS_AMOUNT);

        usdc.mint(trader, traderFunds);
        vm.prank(trader);
        usdc.approve(address(handler), traderFunds);

        IMatchHandler.Investor memory selfBuyer = _makeBuyer();
        selfBuyer.wallet = trader;

        vm.prank(operator);
        handler.matchOrder(
            address(dsToken),
            address(usdc),
            trader,
            DS_AMOUNT,
            USDC_AMOUNT,
            SELLER_FEE,
            BUYER_FEE,
            selfBuyer
        );

        assertEq(dsToken.balanceOf(trader), DS_AMOUNT, "DS token transfer nets to zero");
        assertEq(usdc.balanceOf(trader), USDC_AMOUNT - SELLER_FEE, "only combined fees leave trader");
        assertEq(usdc.balanceOf(custodial), SELLER_FEE + BUYER_FEE, "custodial receives fees");
    }
```

**Recommended Mitigation:** Enforce distinct counterparties in `matchOrder`:

```solidity
if (seller == buyer.wallet) revert InvalidCounterparties();
```

**Securitize:** Fixed in commit [`https://github.com/securitize-io/bc-ats-sc/commit/36a9bfda57af4b23523717b781347717a570326c`](https://github.com/securitize-io/bc-ats-sc/commit/36a9bfda57af4b23523717b781347717a570326c)

**Cyfrin:** Verified.

\clearpage
