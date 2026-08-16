---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-2-10
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: Forwarder can be set to frozen address
vuln_class: []
---

# Forwarder can be set to frozen address

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** Forwarder can be set to frozen address; this is not ideal and can result in lost tokens in a worst-case scenario.

**Proof of Concept:**
```solidity
    function test_freezeHolder_setPayoutForwardAddress_toFrozenForwarder() external {
        address user1 = users[0];
        address forwarder = users[1];
        uint256 amountToMint = 1;

        _whitelistAndMintTokensToUser(user1, amountToMint);
        _whitelistAndMintTokensToUser(forwarder, amountToMint);

        // freeze forwarder
        remoraTokenProxy.freezeHolder(forwarder);

        // forward user1 payouts to frozen address
        remoraTokenProxy.setPayoutForwardAddress(user1, forwarder);

        uint64 payoutDistributionAmount = 100e6;
        _fundPayoutToPaymentSettler(payoutDistributionAmount);

        // user1 must have 0 payout because it is forwarding to `forwarder`
        uint256 user1PayoutBalance = remoraTokenProxy.payoutBalance(user1);
        assertEq(user1PayoutBalance, 0);

        // forwarder is frozen  so receives no forwarded payout
        uint256 forwarderPayoutBalance = remoraTokenProxy.payoutBalance(forwarder);
        assertEq(forwarderPayoutBalance, 0);

        // remove the forwarding while forwarder still frozen
        remoraTokenProxy.removePayoutForwardAddress(user1);

        // user1 can't claim any tokens - user1 has lost their payouts
        user1PayoutBalance = remoraTokenProxy.payoutBalance(user1);
        assertEq(user1PayoutBalance, 0);
    }
```

**Recommended Mitigation:** `DividendManager::setPayoutForwardAddress` should revert if `forwardingAddress` is frozen. When an address is frozen if that address has users forwarding to it, consider cancelling all those forwards.

**Remora:** Acknowledged; the forwarding mechanism is only intended to be used by Remora protocol-owned address to forward payout distributions from tokens held by the `TokenBank` and our liquidity pools. So it is unlikely that the freezing and forwarding mechanisms will ever interact.
