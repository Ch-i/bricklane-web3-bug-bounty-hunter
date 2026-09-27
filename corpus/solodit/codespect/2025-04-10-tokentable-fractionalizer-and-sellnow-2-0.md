---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-04-10-tokentable-fractionalizer-and-sellnow-2-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-04-10T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-10-TokenTable-Fractionalizer-and-SellNow.md
tags:
- firm:codespect
- report:2025-04-10-tokentable-fractionalizer-and-sellnow
title: '[M-01] DOS in BuyerAggregator’s confirm function'
vuln_class: []
---

# [M-01] DOS in BuyerAggregator’s confirm function

_Section severity (from Solodit section header): Medium_  
_Audit firm: CODESPECT_  
_Source report: [2025-04-10-TokenTable-Fractionalizer-and-SellNow.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-10-TokenTable-Fractionalizer-and-SellNow.md)_

---

**Files:** [BuyerAggregator.sol](https://github.com/EthSign/tokentable-sellnow-swap-evm/blob/101eff63f094aafd9f5ea7bcd1025acba2e272f0/src/BuyerAggregator.sol)

**Description:**

Users are supposed to call the `confirm()` function in `BuyerAggregator` when they have collected the required amount to buy the NFT:

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

However, there is a check that the contract's token balance must be equal to the `expectedAmount`. That means that malicious users can always send as little as 1 wei to the contract to DOS this function call.

**Impact:** An attacker can DOS the `confirm()` function call by frontrunning the transaction and sending 1 wei of the token. Even if users `withdrawDeposit(...)` to make the balance correct again, the malicious user can repeat the attack.

**Recommendation(s):** Make the check confirm that the contract's token balance is `>=` to the `expectedAmount`.

**Status:** Fixed

**Update from TokenTable:** [030d772345c18f08c79dfbab9dd9fffe89772763](https://github.com/EthSign/tokentable-sellnow-swap-evm/pull/11/commits/030d772345c18f08c79dfbab9dd9fffe89772763)
