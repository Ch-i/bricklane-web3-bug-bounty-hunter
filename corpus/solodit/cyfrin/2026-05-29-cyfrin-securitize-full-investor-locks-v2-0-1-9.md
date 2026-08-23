---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-29-cyfrin-securitize-full-investor-locks-v2-0-1-9
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-05-29T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-29-cyfrin-securitize-full-investor-locks-v2-0
title: Platform-wallet routing bypasses the `NOT_ENOUGH_INVESTORS` minimum-total-population
  floor on full-exit transfers
vuln_class: []
---

# Platform-wallet routing bypasses the `NOT_ENOUGH_INVESTORS` minimum-total-population floor on full-exit transfers

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md)_

---

**Description:** `completeTransferCheck` at lines 409-416 enforces a minimum-total-population floor: an existing investor cannot fully exit if the total population is at or below the configured minimum AND the recipient is an existing investor (not a new one):

```solidity
if (
    _args.fromInvestorBalance == _args.value &&            // sender fully depletes
    !isNewInvestor(toInvestorBalance) &&                   // recipient is not new
    getTotalInvestorsCount() <= getMinimumTotalInvestors()
) {
    return (71, NOT_ENOUGH_INVESTORS);
}
```

The check protects the population floor encoded by `getMinimumTotalInvestors()` (which may be a regulatory eligibility threshold for specific fund structures or exemptions). The clause `fromInvestorBalance == value` keys on the IMMEDIATE sender's full-depletion status, not the original holder's. Routing through a platform wallet breaks the enforcement:

- Leg 1 (X to platform, full balance): the platform-recipient short-circuit at `doPreTransferCheckRegulated:227-238` returns `(0, VALID)` after only the force-full-transfer guard. `completeTransferCheck` is skipped, so the `NOT_ENOUGH_INVESTORS` check at lines 409-416 never runs. `recordTransfer` then runs `adjustTotalInvestorsCounts(_from, Decrease)` because `compareInvestorBalance(X, value, value) = true` (X's post-balance is 0). X is decremented out of `totalInvestors`.
- Leg 2 (platform to existing_Y): `completeTransferCheck` runs. `_args.fromInvestorBalance = balanceOfInvestor(platform)`, and because platform wallets have no investor record (`getInvestor(platform) = ""` and `token.balanceOfInvestor("") = 0`), `_args.fromInvestorBalance = 0`. The first clause `_args.fromInvestorBalance == _args.value` evaluates as `0 == _args.value`, which is false for any positive transfer. The check is skipped. `recordTransfer` then evaluates `compareInvestorBalance(Y, value, 0)`, which returns false because Y's pre-transfer balance was positive. No increment fires on Y's side.

End state: X is gone from `totalInvestors`, Y is unchanged, total population dropped by 1. If the population was at exactly `getMinimumTotalInvestors`, it now drops below the configured floor.

**Files:**

- `contracts/compliance/ComplianceServiceRegulated.sol` (`completeTransferCheck` lines 409-416; `doPreTransferCheckRegulated` short-circuit at 227-238)

**Impact:** An existing investor can fully exit a regulated token even when `getTotalInvestorsCount() <= getMinimumTotalInvestors()` by routing the transfer through a platform wallet. Concrete example: configured minimum is 10, current count is 10, X wants to exit. Direct `X.transfer(existing_Y, full_balance)` reverts with `(71, NOT_ENOUGH_INVESTORS)`. Routed: `X.transfer(platform, full_balance)` succeeds via the platform-recipient short-circuit (count drops from 10 to 9), then `platform.transfer(existing_Y, full_balance)` succeeds because `fromInvestorBalance == 0 != value` defeats the check. End state: population at 9, below the configured floor of 10. If `getMinimumTotalInvestors` encodes a regulatory population threshold (for fund-eligibility under a Reg-D 506(b) limit or a specific exemption's investor-count requirement), the bypass directly violates that threshold. Master can detect the below-floor state via the population count and intervene by re-issuing tokens to restore the count, but the routing achieves the prohibited state without on-chain enforcement.

**Recommended Mitigation:** Move the `NOT_ENOUGH_INVESTORS` check above the platform-recipient short-circuit so it evaluates before the early return at `doPreTransferCheckRegulated:237`. Add an explicit platform-recipient guard so the routed exit is caught on leg 1:

```solidity
// In doPreTransferCheckRegulated, before the platform-recipient short-circuit:
bool isPlatformWalletTo = IDSWalletManager(_services[WALLET_MANAGER]).isPlatformWallet(_to);
uint256 toInvestorBalanceForExitCheck = balanceOfInvestor(_services, _to);
if (
    fromInvestorBalance == _value &&
    !isPlatformWalletTo &&                                   // platform recipient is not "exit-allowed"
    !isNewInvestor(toInvestorBalanceForExitCheck) &&
    ComplianceServiceRegulated(_services[COMPLIANCE_SERVICE]).getTotalInvestorsCount() <=
    IDSComplianceConfigurationService(_services[COMPLIANCE_CONFIGURATION_SERVICE]).getMinimumTotalInvestors()
) {
    return (71, NOT_ENOUGH_INVESTORS);
}
```

The `!isPlatformWalletTo` clause is required: without it, leg 1's recipient (platform wallet) appears as `isNewInvestor` (because `balanceOfInvestor(platform) = 0`), so the check passes on leg 1 and the routed exit still succeeds. With the clause, leg 1 explicitly blocks full-exit transfers to platform wallets when the population is at or below the floor.

Structurally cleaner: restructure the short-circuit at lines 227-238 to evaluate sender-side population constraints before skipping recipient-side constraints. Shares the fix surface with M-5, M-7, and L-9.


**Securitize:** Acknowledged.

\clearpage
