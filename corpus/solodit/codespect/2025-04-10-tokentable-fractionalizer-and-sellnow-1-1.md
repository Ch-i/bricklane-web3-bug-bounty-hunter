---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-04-10-tokentable-fractionalizer-and-sellnow-1-1
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-04-10T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-10-TokenTable-Fractionalizer-and-SellNow.md
tags:
- firm:codespect
- report:2025-04-10-tokentable-fractionalizer-and-sellnow
title: '[H-02] Fees not considered in expectedAmount inside BuyerAggregator'
vuln_class: []
---

# [H-02] Fees not considered in expectedAmount inside BuyerAggregator

_Section severity (from Solodit section header): High_  
_Audit firm: CODESPECT_  
_Source report: [2025-04-10-TokenTable-Fractionalizer-and-SellNow.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-10-TokenTable-Fractionalizer-and-SellNow.md)_

---

**Files:** [BuyerAggregator.sol](https://github.com/EthSign/tokentable-sellnow-swap-evm/blob/101eff63f094aafd9f5ea7bcd1025acba2e272f0/src/BuyerAggregator.sol#L89-L94)

**Description:**

The `BuyerAggregator` contract is used to collect funds from whitelisted buyers (in ETH or an ERC20 token) for the purpose of purchasing future tokens. The future tokens are later fractionalized via the `ShareFractionalizer`. The type of token to be deposited depends on the `SellNow` session configuration. Once the required amount is collected, the `confirm(...)` function is called to finalize the process. This action:

1. Locks the aggregator from further deposits;
2. Calls `sellNow.confirm(...)` to proceed with the buyer-side confirmation;

The issue lies in how the aggregator checks whether the required amount of tokens has been collected. In the `confirm(...)` function, the aggregator compares its current balance against `expectedAmount`, which is loaded from `sessionConfig.paymentToken.amount`. However, this value does not include session fees.

```solidity
function confirm() external onlyBeforeConfirm {
    confirmed = true;
    address paymentToken = sessionConfig.paymentToken.tokenAddress;
    uint256 expectedAmount = sessionConfig.paymentToken.amount;
    require(
        paymentToken == address(0)
            ? address(this).balance == expectedAmount
            : IERC20(paymentToken).balanceOf(address(this)) == expectedAmount,
        IncorrectPaymentAmount()
    );
    sellNowInstance.confirm(sessionId);
}
```

As a result, when `sellNow.confirm(sessionId)` is called, the aggregator might not have enough funds to cover both the token price and the associated fees. This leads to a revert, even though the aggregator believes the full amount has been collected.

**Impact:** Denial of service of the selling process: the aggregator will be unable to confirm the session if fees are not accounted for in the `expectedAmount`.

**Recommendation(s):** Update the aggregator's `confirm(...)` logic to include any applicable session fees in the required balance check.

**Status:** Fixed

**Update from TokenTable:** [887d94a2a456bbece39074bf63ced2c33d203646](https://github.com/EthSign/tokentable-sellnow-swap-evm/pull/11/commits/887d94a2a456bbece39074bf63ced2c33d203646)
