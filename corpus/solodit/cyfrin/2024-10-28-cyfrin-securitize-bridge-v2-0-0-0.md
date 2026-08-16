---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-10-28-cyfrin-securitize-bridge-v2-0-0-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-10-28T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-28-cyfrin-securitize-bridge-v2.0.md
tags:
- firm:cyfrin
- report:2024-10-28-cyfrin-securitize-bridge-v2-0
title: Allow message value to be more than the quote cost
vuln_class: []
---

# Allow message value to be more than the quote cost

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-10-28-cyfrin-securitize-bridge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-28-cyfrin-securitize-bridge-v2.0.md)_

---

**Description:** The `SecuritizeBridge` contract's `bridgeDSTokens()` function requires users to provide an exact value that matches the quote obtained from `quoteBridge()`. This strict matching requirement creates issues because the actual cost can change between when a user checks the quote and when they submit their transaction.
```solidity
    function bridgeDSTokens(uint16 targetChain, uint256 value) public override payable whenNotPaused {
        uint256 cost = quoteBridge(targetChain);
        require(msg.value == cost, "Transaction value should be equal to quoteBridge response");
...
    }
```
The cost calculation depends on multiple factors as shown in Wormhole's `DeliveryProvider` contract [here](https://github.com/wormhole-foundation/wormhole/blob/abd0b330efa0a1bc86f0914396cbd570c99cdf1a/relayer/ethereum/contracts/relayer/deliveryProvider/DeliveryProvider.sol#L28), including gas prices on the target chain and asset conversion rates. These values can fluctuate frequently based on network conditions.

```solidity
    function quoteEvmDeliveryPrice(
        uint16 targetChain,
        Gas gasLimit,
        TargetNative receiverValue
    )
        public
        view
        returns (LocalNative nativePriceQuote, GasPrice targetChainRefundPerUnitGasUnused)
    {
        // Calculates the amount to refund user on the target chain, for each unit of target chain gas unused
        // by multiplying the price of that amount of gas (in target chain currency)
        // by a target-chain-specific constant 'denominator'/('denominator' + 'buffer'), which will be close to 1

        (uint16 buffer, uint16 denominator) = assetConversionBuffer(targetChain);
        targetChainRefundPerUnitGasUnused = GasPrice.wrap(gasPrice(targetChain).unwrap() * (denominator) / (uint256(denominator) + buffer));

        // Calculates the cost of performing a delivery with 'gasLimit' units of gas and 'receiverValue' wei delivered to the target contract

        LocalNative gasLimitCostInSourceCurrency = quoteGasCost(targetChain, gasLimit);
        LocalNative receiverValueCostInSourceCurrency = quoteAssetCost(targetChain, receiverValue);
        nativePriceQuote = quoteDeliveryOverhead(targetChain) + gasLimitCostInSourceCurrency + receiverValueCostInSourceCurrency;

        // Checks that the amount of wei that needs to be sent into the target chain is <= the 'maximum budget' for the target chain

        TargetNative gasLimitCost = gasLimit.toWei(gasPrice(targetChain)).asTargetNative();
        if(receiverValue.asNative() + gasLimitCost.asNative() > maximumBudget(targetChain).asNative()) {
            revert ExceedsMaximumBudget(targetChain, receiverValue.unwrap() + gasLimitCost.unwrap(), maximumBudget(targetChain).unwrap());
        }
    }
```
When the cost changes even slightly between the quote check and transaction submission, the transaction fails. This creates a poor user experience where transactions frequently revert despite users attempting to pay the correct amount.

A malicious actor could worsen this issue by manipulating network conditions to cause price fluctuations, effectively preventing other users from successfully bridging their assets.

**Impact:** Users face failed transactions when attempting to bridge assets causing frustration. In extreme cases, attackers could temporarily prevent specific users from bridging assets by manipulating conditions to cause price fluctuations.

**Recommended Mitigation:** Modify the function to accept value that exceed the current quote and automatically refund any excess amount back to the user. This approach provides flexibility to handle minor price fluctuations while ensuring users don't overpay.

**Securitize:** Fixed in commit [d3b97a](https://bitbucket.org/securitize_dev/bc-securitize-bridge-sc/commits/d3b97a76f93fd80ed6401372eadf206e1fb5d864) and [221759](https://bitbucket.org/securitize_dev/bc-securitize-bridge-sc/commits/2217591277f5a52913e0cd82136de13607608123).

**Cyfrin:** Verified.

\clearpage
