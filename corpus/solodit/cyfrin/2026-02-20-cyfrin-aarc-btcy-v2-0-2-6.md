---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-20-cyfrin-aarc-btcy-v2-0-2-6
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-02-20T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-20-cyfrin-aarc-btcy-v2-0
title: Rename `Deposit::amountDepositedMinusFees` since subscription fee only used
  to emit event but not subtracted from amount deposited
vuln_class: []
---

# Rename `Deposit::amountDepositedMinusFees` since subscription fee only used to emit event but not subtracted from amount deposited

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-20-cyfrin-aarc-btcy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md)_

---

**Description:** In `IBTCYHub::_processSubscription` the fee is calculated but it is never used or subsequently deducted from the tokens minted to the user:
```solidity
        // @audit comment indicates fee only for events, potentially used off-chain
        // Calculate subscription fee for accounting (not deducted, just for events)
        uint256 feeRate =
            data.operationTypes[i] == OperationType.INSTANT ? $.instantSubscriptionFee : $.regularSubscriptionFee;
        // @audit calculated fee never actually used
        uint256 fee = _getSubscriptionFees(feeRate, processedAmount);

        // Calculate mint amount based on processed subscription amount
        // @audit doesn't take into account fee
        uint256 ibtcyOwed = _getMintAmountForPrice(processedAmount, data.prices[i]);

        // @audit mints full amount to user, doesn't deduct fee, fee never sent anywhere just to emit event
        // Mint tokens to captured user
        $.ibtcy.mint(user, ibtcyOwed);
```

In contrast `_processRedemption` returns fees, `_processRedemptionBatch` sums up the total fees and `processRedemptions` sends them to the fee recipient.

It is also confusing that the storage slot subsequently updated is called `depositor.amountDepositedMinusFees` even though no fee is subtracted:
```solidity
        // Update depositor amount
        unchecked {
            uint256 remainingDepositAmount = depositorAmount - processedAmount;
            if (remainingDepositAmount != 0) {
                depositor.amountDepositedMinusFees = remainingDepositAmount;
            } else {
                delete $.depositIdToDepositor[depositId];
            }
        }
```

If the fee is only for event generation and used off-chain, then consider renaming `Deposit::amountDepositedMinusFees` to `amountDeposited` since fees aren't subtracted from that amount.

**Aarc:** Fixed in commit [f040e83](https://github.com/aarc-xyz/btcy-contracts-main/commit/f040e8357de935359e8219cf41133af047b81f95).

**Cyfrin:** Verified.
