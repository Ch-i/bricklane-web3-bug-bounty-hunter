---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-01-10-cyfrin-thermae-1-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-01-10T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-10-cyfrin-thermae.md
tags:
- firm:cyfrin
- report:2024-01-10-cyfrin-thermae
title: No precision scaling or minimum received amount check when subtracting `relayerFeeAmount`
  can revert due to underflow or return less tokens to user than specified
vuln_class: []
---

# No precision scaling or minimum received amount check when subtracting `relayerFeeAmount` can revert due to underflow or return less tokens to user than specified

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-01-10-cyfrin-thermae.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-10-cyfrin-thermae.md)_

---

**Description:** `PorticoFinish::payOut` L376 attempts to subtract the `relayerFeeAmount` from the final post-bridge and post-swap token balance:
```solidity
finalUserAmount = finalToken.balanceOf(address(this)) - relayerFeeAmount;
```

There is [no precision scaling](https://dacian.me/precision-loss-errors#heading-no-precision-scaling) to ensure that `PorticoFinish`'s token contract balance and `relayerFeeAmount` are in the same decimal precision; if the `relayerFeeAmount` has 18 decimal places but the token is USDC with only 6 decimal places, this can easily revert due to underflow resulting in the bridged tokens being stuck.

An excessively high `relayerFeeAmount` could also significantly reduce the amount of post-bridge and post-swap tokens received as there is no check on the minimum amount of tokens the user will receive after deducting `relayerFeeAmount`. This current configuration is an example of the ["MinTokensOut For Intermediate, Not Final Amount"](https://dacian.me/defi-slippage-attacks#heading-mintokensout-for-intermediate-not-final-amount) vulnerability class; as the minimum received tokens check is before the deduction of `relayerFeeAmount` a user will always receive less tokens than their specified minimum if `relayerFeeAmount > 0`.

**Impact:** Bridged tokens stuck or user receives less tokens than their specified minimum.

**Recommended Mitigation:** Ensure that token balance and `relayerFeeAmount` have the same decimal precision before combining them. Alternatively check for underflow and don't charge a fee if this would be the case. Consider enforcing the user-specified minimum output token check again when deducting `relayerFeeAmount`, and if this would fail then decrease `relayerFeeAmount` such that the user at least receives their minimum specified token amount.

Another option is to check that even if it doesn't underflow, that the remaining amount after subtracting `relayerFeeAmount` is a high percentage of the bridged amount; this would prevent a scenario where `relayerFeeAmount` takes a large part of the bridged amount, effectively capping `relayerFeeAmount` to a tiny % of the post-bridge and post-swap funds. This scenario can still result in the user receiving less tokens than their specified minimum however.

From the point of view of the smart contract, it should protect itself against the possibility of the token amount and `relayerFeeAmount` being in different decimals or that `relayerFeeAmount` would be too high, similar to how for example L376 inside `payOut` doesn't trust the bridge reported amount and checks the actual token balance.

**Wormhole:**
Fixed in commit 05ba84d by adding an underflow check. Any misbehavior is due to bad user input and should be corrected off-chain. Only the user is able to set the relayer fee in the input parameters.

**Cyfrin:** Verified potential underflow due to mismatched precision between relayer fee & token amount is now handled. The implementation now favors the relayer however this is balanced by the fact that only the user can set the relayer fee, so the attack surface is limited to self-inflicted harm. If in the future another entity such as the relayer could set the relayer fee then this could be used to drain the bridged tokens, but with the current implementation this is not possible unless the user sets an incorrectly large relayer fee which is self-inflicted.

\clearpage
