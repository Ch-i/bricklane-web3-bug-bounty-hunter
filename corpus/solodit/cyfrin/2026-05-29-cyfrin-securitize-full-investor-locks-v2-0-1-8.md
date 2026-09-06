---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-29-cyfrin-securitize-full-investor-locks-v2-0-1-8
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-05-29T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-29-cyfrin-securitize-full-investor-locks-v2-0
title: Platform-wallet routing bypasses three sender-side held-token min-balance checks
  in `completeTransferCheck`
vuln_class: []
---

# Platform-wallet routing bypasses three sender-side held-token min-balance checks in `completeTransferCheck`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md)_

---

**Description:** Three sender-side minimum-balance checks in `completeTransferCheck` enforce that a partial transfer cannot leave the sender below a configured minimum-holdings floor. All three evaluate the IMMEDIATE sender's post-transfer balance, not the original holder's, so routing through a platform wallet skips them.

**Component 1: US sender min-holdings (`getMinUSTokens`).** At lines 279-283, inside `if (_args.fromRegion == US)`:

```solidity
if (
    _args.fromInvestorBalance > _args.value &&
    _args.fromInvestorBalance - _args.value < getMinUSTokens()
) {
    return (51, AMOUNT_OF_TOKENS_UNDER_MIN);
}
```

For platform sender, `_args.fromRegion = NONE` (platform wallets have no country), so the US branch never runs.

**Component 2: EU sender min-holdings (`getMinEUTokens`).** At lines 317-321, inside `if (_args.fromRegion == EU)`:

```solidity
if (
    _args.fromInvestorBalance - _args.value < getMinEUTokens() &&
    _args.fromInvestorBalance > _args.value
) {
    return (51, AMOUNT_OF_TOKENS_UNDER_MIN);
}
```

Same shape as Component 1: platform sender's region is NONE, EU branch never runs.

**Component 3: General per-investor sender min-holdings (`getMinimumHoldingsPerInvestor`).** At lines 418-424, region-agnostic, with explicit platform-sender guard:

```solidity
if (
    !isPlatformWalletFrom &&
    _args.fromInvestorBalance - _args.value < getMinimumHoldingsPerInvestor() &&
    _args.fromInvestorBalance > _args.value
) {
    return (51, AMOUNT_OF_TOKENS_UNDER_MIN);
}
```

The `!isPlatformWalletFrom` guard intentionally exempts platform-as-sender, but does not address the X-via-platform routing case.

Routing through a platform wallet breaks enforcement of all three:

- Leg 1 (X to platform): the platform-recipient short-circuit at `doPreTransferCheckRegulated:227-238` returns `(0, VALID)` after only the force-full-transfer guard. `completeTransferCheck` is skipped, so none of the three sender-side min checks run against X's post-transfer balance.
- Leg 2 (platform to Y): the platform is now the sender. Component 1 is gated on `fromRegion == US` (skipped, region is NONE), Component 2 on `fromRegion == EU` (skipped), Component 3 on `!isPlatformWalletFrom` (skipped, sender is platform). None re-evaluate against the original holder X.

End state: X retains a sub-minimum balance even though a direct partial transfer of the same value would have reverted with `AMOUNT_OF_TOKENS_UNDER_MIN`.

**Files:**

- `contracts/compliance/ComplianceServiceRegulated.sol` (`completeTransferCheck` lines 279-283, 317-321, 418-424; `doPreTransferCheckRegulated` short-circuit at 227-238)

**Impact:** A US, EU, or any-region investor can drop below their configured minimum-holdings floor by partial-transferring through a platform wallet. Concrete example: investor X holds 1000 tokens, `getMinUSTokens() = 100`. Direct `transfer(Y, 950)` reverts because `1000 - 950 = 50 < 100`. Routed: `X.transfer(platform, 950)` succeeds via the platform-recipient short-circuit, then `platform.transfer(Y, 950)` succeeds because the sender-side checks are skipped on the platform-as-sender leg. X retains 50 (below min). The same shape applies to `getMinEUTokens` for EU senders and `getMinimumHoldingsPerInvestor` for any-region senders. Master can detect the below-min state via off-chain monitoring and call `recordSeize` to restore the floor, but the bypass occurred without on-chain enforcement and the configured minimum-holdings policy is silently violated until intervention.

**Recommended Mitigation:** Move the three sender-side min-balance checks above the platform-recipient short-circuit in `doPreTransferCheckRegulated`, so they evaluate before the early return at line 237:

```solidity
// In doPreTransferCheckRegulated, evaluate sender-side min-balance constraints
// before the platform-recipient short-circuit.
if (fromRegion == US &&
    fromInvestorBalance > _value &&
    fromInvestorBalance - _value < cfg.getMinUSTokens()) {
    return (51, AMOUNT_OF_TOKENS_UNDER_MIN);
}
if (fromRegion == EU &&
    fromInvestorBalance > _value &&
    fromInvestorBalance - _value < cfg.getMinEUTokens()) {
    return (51, AMOUNT_OF_TOKENS_UNDER_MIN);
}
if (!IDSWalletManager(_services[WALLET_MANAGER]).isPlatformWallet(_from) &&
    fromInvestorBalance > _value &&
    fromInvestorBalance - _value < cfg.getMinimumHoldingsPerInvestor()) {
    return (51, AMOUNT_OF_TOKENS_UNDER_MIN);
}

// Then the existing platform-recipient short-circuit.
```

Structurally cleaner: restructure the short-circuit at lines 227-238 to only skip RECIPIENT-side checks (caps, region restrictions on recipient, recipient-side min/max), preserving sender-side enforcement uniformly. Sender-side constraints (Reg-D lockup, flowback, min-holdings) should evaluate on every transfer regardless of recipient type. This shares the fix surface with M-5 (Reg-D lockup), M-7 (flowback), and L-7 (cap-skip clause asymmetry).


**Securitize:** Acknowledged.
