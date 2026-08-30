---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-20-cyfrin-aarc-btcy-v2-0-3-10
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-02-20T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-20-cyfrin-aarc-btcy-v2-0
title: More efficient implementations of `IBTCYHub::processSubscriptions, processRedemptions`
vuln_class: []
---

# More efficient implementations of `IBTCYHub::processSubscriptions, processRedemptions`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-20-cyfrin-aarc-btcy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md)_

---

**Description:** More efficient implementations of `IBTCYHub::processSubscriptions, processRedemptions`, see the before & after:
```diff
forge test --gas-report

- | processSubscriptions               | 10880           | 114636 | 126229 | 166875 | 117     |
+ | processSubscriptions               | 10880           | 114022 | 125581 | 166161 | 117     |

- | processRedemptions                 | 3691            | 77552  | 89690  | 123840 | 43      |
+ | processRedemptions                 | 3691            | 77036  | 89038  | 123188 | 43      |
```

Primarily achieved by avoiding copying `calldata` into `memory` unnecessarily while still not triggering `stack-too-deep` errors. The code is also simpler and allows deletion of some structs and helper functions.
```solidity
    function processSubscriptions(
        bytes32[] calldata depositIds,
        uint256[] calldata priceIds,
        uint256[] calldata subscriptionAmounts,
        OperationType[] calldata operationTypes
    ) external override onlyRole(MANAGER_ROLE) nonReentrant whenNotPaused {
        require(depositIds.length == priceIds.length, ArrayLengthMismatch());
        require(depositIds.length == subscriptionAmounts.length, ArrayLengthMismatch());
        require(depositIds.length == operationTypes.length, ArrayLengthMismatch());

        IBTCYHubStorage storage $ = _getIBTCYHubStorage();
        (uint256[] memory prices, uint256[] memory timestamps) = $.pricer.getPriceInfos(priceIds);

        for (uint256 i; i < depositIds.length;) {
            _processSubscription($, depositIds[i], prices[i], subscriptionAmounts[i], operationTypes[i], timestamps[i]);
            unchecked {
                ++i;
            }
        }
    }

    function _processSubscription(
        IBTCYHubStorage storage $,
        bytes32 depositId,
        uint256 price,
        uint256 subscriptionAmount,
        OperationType operationType,
        uint256 priceTimestamp)
    internal {
        Depositor storage depositor = $.depositIdToDepositor[depositId];
        address user = depositor.user;

        // Check if deposit ID is valid
        require(user != address(0), InvalidDepositId());
        require(block.timestamp - priceTimestamp <= MAX_PRICE_AGE, PriceTooOld());

        // Get depositor amount and validate subscription amount
        uint256 depositorAmount = depositor.amountDepositedMinusFees;
        require(
            subscriptionAmount <= depositorAmount,
            SubscriptionAmountCannotBeGreaterThanDeposited(subscriptionAmount, depositorAmount)
        );

        // Calculate subscription fee for accounting (not deducted, just for events)
        uint256 feeRate =
            operationType == OperationType.INSTANT ? $.instantSubscriptionFee : $.regularSubscriptionFee;
        uint256 fee = _getSubscriptionFees(feeRate, subscriptionAmount);

        // Calculate mint amount based on processed subscription amount
        uint256 ibtcyOwed = _getMintAmountForPrice(subscriptionAmount, price);

        // Mint tokens to captured user
        $.ibtcy.mint(user, ibtcyOwed);

        // Update depositor amount
        unchecked {
            uint256 remainingDepositAmount = depositorAmount - subscriptionAmount;
            if (remainingDepositAmount != 0) {
                depositor.amountDepositedMinusFees = remainingDepositAmount;
            } else {
                delete $.depositIdToDepositor[depositId];
            }
        }

        emit MintCompleted(user, depositId, subscriptionAmount, ibtcyOwed, fee, operationType);
    }

    function processRedemptions(
        bytes32[] calldata redemptionIds,
        uint256[] calldata priceIds,
        uint256[] calldata redemptionAmounts,
        OperationType[] calldata operationTypes
    ) external override onlyRole(MANAGER_ROLE) nonReentrant whenNotPaused {
        require(redemptionIds.length == priceIds.length, ArrayLengthMismatch());
        require(redemptionIds.length == redemptionAmounts.length, ArrayLengthMismatch());
        require(redemptionIds.length == operationTypes.length, ArrayLengthMismatch());

        IBTCYHubStorage storage $ = _getIBTCYHubStorage();
        require(!$.redemptionPaused, RedemptionsPaused());

        // Get price information and create batch data
        (uint256[] memory prices, uint256[] memory timestamps) = $.pricer.getPriceInfos(priceIds);

        (uint256 totalFeesInIBTCY, uint256 totalIBTCYTokensToBurn) =
            _processRedemptions($, redemptionIds, prices, redemptionAmounts, operationTypes, timestamps);

        // Transfer fees in iBTCY to feeRecipient
        if (totalFeesInIBTCY != 0) {
            IERC20(address($.ibtcy)).safeTransfer($.feeRecipient, totalFeesInIBTCY);
        }

        // Burn remaining iBTCY held by the hub
        $.ibtcy.burn(totalIBTCYTokensToBurn);
    }

    // required to avoid stack-too-deep
    function _processRedemptions(
        IBTCYHubStorage storage $,
        bytes32[] calldata redemptionIds,
        uint256[] memory prices,
        uint256[] calldata redemptionAmounts,
        OperationType[] calldata operationTypes,
        uint256[] memory timestamps)
    internal returns(uint256 totalFeesInIBTCY, uint256 totalIBTCYTokensToBurn) {
        for (uint256 i; i < redemptionIds.length;) {
            (uint256 fee, uint256 processedAmount) = _processRedemption($,
                                                                        redemptionIds[i],
                                                                        prices[i],
                                                                        redemptionAmounts[i],
                                                                        operationTypes[i],
                                                                        timestamps[i]);
            totalFeesInIBTCY += fee;
            totalIBTCYTokensToBurn += processedAmount;
            unchecked {
                ++i;
            }
        }
    }

    function _processRedemption(
        IBTCYHubStorage storage $,
        bytes32 redemptionId,
        uint256 price,
        uint256 redemptionAmount,
        OperationType operationType,
        uint256 priceTimestamp)
        internal
        returns (uint256 feeInIBTCY, uint256 ibtcyToBurn)
    {
        // Check if redemption ID is valid
        Redeemer storage redeemer = $.redemptionIdToRedeemer[redemptionId];

        // Capture user address before any modifications
        address user = redeemer.user;
        require(user != address(0), InvalidRedemptionId());
        require(block.timestamp - priceTimestamp <= MAX_PRICE_AGE, PriceTooOld());

        // Validate and process amounts
        uint256 redeemerAmount = redeemer.amountRwaTokenBurned;
        require(
            redemptionAmount <= redeemerAmount,
            RedemptionAmountCannotBeGreaterThanBurned(redemptionAmount, redeemerAmount)
        );

        // Calculate fee and burn amounts
        {
            uint256 feeRate =
                operationType == OperationType.INSTANT ? $.instantRedemptionFee : $.regularRedemptionFee;
            feeInIBTCY = _getRedemptionFees(feeRate, redemptionAmount);
            ibtcyToBurn = redemptionAmount - feeInIBTCY;
        }

        // Update redeemer state
        unchecked {
            uint256 remainingRedemptionAmount = redeemerAmount - redemptionAmount;
            if (remainingRedemptionAmount != 0) {
                redeemer.amountRwaTokenBurned = remainingRedemptionAmount;
            } else {
                delete $.redemptionIdToRedeemer[redemptionId];
            }
        }

        // Emit event with BTC amount for off-chain distribution
        emit RedemptionCompleted(user, redemptionId, ibtcyToBurn,
                                _getRedemptionAmountForRwa(ibtcyToBurn, price), feeInIBTCY, operationType);
    }
```

**Aarc:** Fixed in commit [b2bad22](https://github.com/aarc-xyz/btcy-contracts-main/pull/13/changes/b2bad22526252a68554bee38b91cbf42b5cae382).

**Cyfrin:** Verified.
