---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-4-4
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-03-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-25-cyfrin-sablier-bob-escrow-v2-0
title: Attacker can permanently lock or drain fee-on-transfer tokens from `SablierEscrow`
vuln_class: []
---

# Attacker can permanently lock or drain fee-on-transfer tokens from `SablierEscrow`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md)_

---

**Description:** The `SablierEscrow` is a contract that enables peer-to-peer trading between users to swap ERC-20 tokens with each other. The contract allows users to create, cancel and fill orders anytime. When creating orders, the contract does not handle the case where the `sellToken` is a fee-on-transfer token.

This leads to a case where the `_orders` mapping stores an inflated `sellAmount` than the actual `sellToken` amount received by the contract in the subsequent transfer.
```solidity
        // Effect: create the order.
        _orders[orderId] = Escrow.Order({
            seller: msg.sender,
            buyer: buyer,
            sellToken: sellToken,
            buyToken: buyToken,
            sellAmount: sellAmount,
            minBuyAmount: minBuyAmount,
            expiryTime: expiryTime,
            wasCanceled: false,
            wasFilled: false
        });

        // Interaction: transfer sell tokens from caller to this contract.
        sellToken.safeTransferFrom(msg.sender, address(this), sellAmount);
```

When cancelling or filling the order using functions `SablierEscrow::cancelOrder` and `SablierEscrow::fillOrder`, it would transfer out the stored inflated `sellAmount` from the `_orders` mapping. If existing orders for the same token exist, the inflated amount will tap into the balance of these other orders. If no other order exists, the tokens remain permanently locked in the contract.

**Impact:** All fee-on-transfer tokens can be drained or remain permanently locked in the contract.

The issue is rated as Informational-severity since fee on transfer tokens are explicitly not supported per the "Protocol Risks" section of the [documentation](https://www.notion.so/sablier-labs/2026-19-02-Sablier-Bob-301f46a1865c804c8806e4c961d190f2?source=copy_link#301f46a1865c80babbadde77b96a3fad) which states:

`Should we evaluate risks due to fee-on-transfer tokens? | No`

However since tokens such as USDT (which includes a fee-activation switch) and stETH (which has the 1-2 wei corner case on transfers as per the [Lido documentation](https://docs.lido.fi/guides/lido-tokens-integration-guide/#1-2-wei-corner-case)) are in-scope, we considered to report this finding.

**Proof of Concept:** Let's take a simple scenario to understand the issue:
 - Assume token A is a fee-on-transfer token with 2% fee.
 - Alice places an order to sell token A with `sellAmount` passed as 10e18. The contract stores `sellAmount` as 10e18 however the escrow only holds 8e18 tokens.
 - Malicious Bob creates an order to sell token A with similar parameters. The contract now holds a balance of 8e18 + 8e18 = 16e18 tokens.
 - Bob cancels his order and receives 10e18 from the contract, leaving 6e18 tokens in the escrow.
 - Bob continues this process until all tokens have been drained from the contract.
 - Alice still has an open order but the order can neither be filled nor cancelled at this point.

**Recommended Mitigation:** Consider checking the balance of the `sellToken` before and after the transfer. Use the difference the store the final `sellAmount` received in the `_orders` mapping. Alternatively, if such tokens are not intended to be supported in the SablierEscrow, consider acknowledging this finding.

**Sablier:** Fee on transfer tokens are explicitly not supported; if users deposit tokens which may have fee-on-transfer enabled in the future, they do this at their own risk.
