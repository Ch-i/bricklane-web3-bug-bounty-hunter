---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-2-9
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: Forwarder can be frozen and still receive and claim payouts while frozen
vuln_class: []
---

# Forwarder can be frozen and still receive and claim payouts while frozen

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** If the forwarder is frozen before the first payout then they don't receive and can't claim any payouts while frozen.

But if the forwarder is frozen after the first payout, then they do receive and can claim payouts while frozen.

**Proof of Concept:**
```solidity
function test_forwarderFrozenBeforeFirstPayout_noPayoutBalanceWhileFrozen() external {
    address user1 = users[0];
    address forwarder = users[1];
    uint256 amountToMint = 1;

    _whitelistAndMintTokensToUser(user1, amountToMint);
    _whitelistAndMintTokensToUser(forwarder, amountToMint);

    remoraTokenProxy.setPayoutForwardAddress(user1, forwarder);

    // forwarder frozen before first distribution payout
    remoraTokenProxy.freezeHolder(forwarder);

    uint64 payoutDistributionAmount = 100e6;
    _fundPayoutToPaymentSettler(payoutDistributionAmount);

    // user1 must have 0 payout because it is forwarding to `forwarder`
    uint256 user1PayoutBalance = remoraTokenProxy.payoutBalance(user1);
    assertEq(user1PayoutBalance, 0);

    // forwarder is frozen yet so receives no forwarded payout
    uint256 forwarderPayoutBalancePreUnfreeze = remoraTokenProxy.payoutBalance(forwarder);
    assertEq(forwarderPayoutBalancePreUnfreeze, 0);
}

function test_forwarderFrozenAfterFirstPayout_validPayoutBalanceWhileFrozen_claimPayoutWhileFrozen() external {
    _fundPayoutToPaymentSettler(1);

    address user1 = users[0];
    address forwarder = users[1];
    uint256 amountToMint = 1;

    _whitelistAndMintTokensToUser(user1, amountToMint);
    _whitelistAndMintTokensToUser(forwarder, amountToMint);

    remoraTokenProxy.setPayoutForwardAddress(user1, forwarder);

    remoraTokenProxy.freezeHolder(forwarder);

    uint64 payoutDistributionAmount = 100e6;
    _fundPayoutToPaymentSettler(payoutDistributionAmount);

    // user1 must have 0 payout because it is forwarding to `forwarder`
    uint256 user1PayoutBalance = remoraTokenProxy.payoutBalance(user1);
    assertEq(user1PayoutBalance, 0);

    // forwarder is frozen yet still receives forwarded payout
    uint256 forwarderPayoutBalance = remoraTokenProxy.payoutBalance(forwarder);
    assertEq(forwarderPayoutBalance, payoutDistributionAmount/2);

    // forwarder claims all their payout
    vm.prank(forwarder);
    remoraTokenProxy.claimPayout();
    assertEq(stableCoin.balanceOf(forwarder), forwarderPayoutBalance);
}
```

**Recommended Mitigation:** The mitigation depends on what the protocol wants to happen in this case, and whether it plans to mitigate L-11. If the protocol wants to allow frozen address to also serve as forwarding addresses and have a payout balance, this could be achieved by:
```diff
    function payoutBalance(address holder) public returns (uint256) {
        HolderManagementStorage storage $ = _getHolderManagementStorage();
        HolderStatus memory rHolderStatus = $._holderStatus[holder];
        uint16 currentPayoutIndex = $._currentPayoutIndex;

+       if ((rHolderStatus.isFrozen && rHolderStatus.frozenIndex == 0) && rHolderStatus.calculatedPayout > 0) return rHolderStatus.calculatedPayout;

        if (
            (!rHolderStatus.isHolder) || //non-holder calling the function
            (rHolderStatus.isFrozen && rHolderStatus.frozenIndex == 0) || //user has been frozen from the start, thus no payout
            rHolderStatus.lastPayoutIndexCalculated == currentPayoutIndex // user has already been paid out up to current payout index
        ) return 0;
```

**Remora:** Acknowledged; the forwarding mechanism is only intended to be used by Remora protocol-owned address to forward payout distributions from tokens held by the `TokenBank` and our liquidity pools. So it is unlikely that the freezing and forwarding mechanisms will ever interact.
