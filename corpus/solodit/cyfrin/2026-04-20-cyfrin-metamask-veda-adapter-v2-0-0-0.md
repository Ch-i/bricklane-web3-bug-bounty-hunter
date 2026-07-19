---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-20-cyfrin-metamask-veda-adapter-v2-0-0-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-04-20T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-20-cyfrin-metamask-veda-adapter-v2.0.md
tags:
- firm:cyfrin
- report:2026-04-20-cyfrin-metamask-veda-adapter-v2-0
title: Front-runner can override withdrawal token and slippage parameters in permissionless
  `VedaAdapter` functions
vuln_class: []
---

# Front-runner can override withdrawal token and slippage parameters in permissionless `VedaAdapter` functions

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-20-cyfrin-metamask-veda-adapter-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-20-cyfrin-metamask-veda-adapter-v2.0.md)_

---

**Description:** `VedaAdapter::withdrawByDelegation` and `VedaAdapter::depositByDelegation` are callable by anyone. The delegation framework's cryptographic signatures and caveats enforce the token being pulled from the delegator and the transfer amount, but do NOT enforce:

1. The withdrawal output token (`_token` parameter in `withdrawByDelegation`)
2. The minimum shares received (`_minimumMint` in `depositByDelegation`)
3. The minimum assets received (`_minimumAssets` in `withdrawByDelegation`)

These parameters are passed as function arguments by the caller and are not part of any signed caveat. A front-runner who observes a pending transaction can extract the delegation chain from the transaction calldata and submit their own transaction with altered parameters. The delegation's `ERC20TransferAmountEnforcer` running total is exhausted by the front-runner's transaction, consuming the single-use delegation.

**Impact:** The delegator receives fair-value assets in an unintended denomination (griefing, not fund theft). Slippage protection is bypassed, though the admin-controlled accountant rate limits practical slippage. The single-use delegation is consumed; the delegator must recreate the delegation chain to retry. The attacker pays gas but gains nothing financially. Practical likelihood is low on Arbitrum due to the centralized sequencer's FIFO ordering.

**Proof of Concept:**
1. Delegator creates a delegation chain for withdrawing 100 vault shares, intending to receive USDC with `_minimumAssets = 990_000000` (~1% slippage tolerance)
2. Front-runner observes the pending `withdrawByDelegation(delegations, USDC, 990_000000)` transaction
3. Front-runner extracts the `delegations` array from calldata and submits `withdrawByDelegation(delegations, WETH, 0)`
4. The delegation framework validates the chain and transfers 100 shares to the adapter (enforced by caveats)
5. The Teller's `withdraw(WETH, 100, 0, rootDelegator)` burns shares and sends WETH (not USDC) to the delegator at the accountant's fair-value rate, with zero slippage protection
6. The delegation's `ERC20TransferAmountEnforcer` running total is exhausted; the original transaction reverts

The same pattern applies to deposits: a front-runner can set `_minimumMint = 0`, removing the delegator's slippage protection.

**Recommended Mitigation:** Include the `_token`, `_minimumMint`, and `_minimumAssets` parameters as enforced fields within the delegation caveats (e.g., via an `AllowedCalldataEnforcer` or a custom enforcer), so these values are cryptographically bound to the delegator's intent and cannot be overridden by the caller.

**MetaMask:** Acknowledged. In our design, the slippage‑related parameters (_minimumMint and _minimumAssets) primarily serve as sanity checks rather than core safety guarantees. While a front‑runner can modify these values, this does not change the underlying economic value of the deposit or withdrawal, as the actual amount transferred is constrained by the delegation framework and vault logic. Regarding the withdrawal token, the VedaVault strictly limits the set of supported tokens. Any attempt to specify an unsupported token will revert, preventing loss of funds even if a front‑runner attempts to alter this parameter. That said, we recognize that reducing the surface for parameter manipulation is desirable. To improve both security and gas efficiency, we are:
- Moving the deposit token configuration into the constructor so it is no longer a user‑supplied parameter in withdrawal calls in commit [`aba8aa5`](https://github.com/MetaMask/delegation-framework/pull/166/changes/aba8aa550ee340718cca670290fcd42f90a1f610)
- Continuing to rely on a private mempool for transaction submission, which significantly mitigates mempool‑based front‑running scenarios

**Cyfrin:** Commit [`aba8aa5`](https://github.com/MetaMask/delegation-framework/pull/166/changes/aba8aa550ee340718cca670290fcd42f90a1f610) verified. `depositToken` is now an immutable address provided in the constructor, no longer a user supplied parameter reducing the risk for manipulation.
