---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-29-cyfrin-securitize-full-investor-locks-v2-0-1-3
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
title: '`ComplianceServiceLibrary::completeTransferCheck` total investors cap-skip
  false for platform-wallet senders'
vuln_class: []
---

# `ComplianceServiceLibrary::completeTransferCheck` total investors cap-skip false for platform-wallet senders

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md)_

---

**Description:** `ComplianceServiceLibrary::completeTransferCheck` at `contracts/compliance/ComplianceServiceRegulated.sol:399-407` enforces the total-investors cap with:

```solidity
if (
    IDSComplianceConfigurationService(_services[COMPLIANCE_CONFIGURATION_SERVICE]).getTotalInvestorsLimit() != 0 &&
    _args.fromInvestorBalance > _args.value &&
    ComplianceServiceRegulated(_services[COMPLIANCE_SERVICE]).getTotalInvestorsCount() >=
    IDSComplianceConfigurationService(_services[COMPLIANCE_CONFIGURATION_SERVICE]).getTotalInvestorsLimit() &&
    isNewInvestor(toInvestorBalance)
) {
    return (40, MAX_INVESTORS_IN_CATEGORY);
}
```

The second conjunct `_args.fromInvestorBalance > _args.value` is the cap-skip clause: when the sender depletes their balance (`fromInvestorBalance == _value`), the sender's `totalInvestors--` at `recordTransfer → adjustTotalInvestorsCounts(_from, Decrease)` offsets the recipient's `+1` increment, leaving `totalInvestors` unchanged across the transfer. In that case the cap should not fire because the net population is constant.

For a platform-wallet sender, `_args.fromInvestorBalance = balanceOfInvestor(_services, _from)` evaluates to `0` because platform wallets have no investor record (`getInvestor(platformWallet) == ""` and `DSToken::balanceOfInvestor("")` returns 0). The cap-skip clause therefore evaluates as `0 > _value` = `false` for any positive transfer, REJECT is skipped, and the transfer is admitted. But platform-wallet senders do not decrement `totalInvestors` either: they aren't counted in the per-investor population at all, so `adjustTotalInvestorsCounts(_from, Decrease)` runs no decrement on the sender leg. The recipient's `+1` increment is unmatched and population grows by one past the configured limit. The cap-skip clause structurally treats platform-wallet senders as offset cases (mimicking the depleter `fromBal == value` shape) when no offset actually happens.

**Files:**

`ComplianceServiceLibrary::completeTransferCheck`

**Impact:** A treasury-distribution from a platform wallet to a fresh investor past `totalInvestorsLimit` is silently admitted instead of reverting with `MAX_INVESTORS_IN_CATEGORY`. Concretely: `totalInvestorsLimit = 100`, `totalInvestorsCount = 100`, issuer transfers 100 tokens from treasury platform-wallet `P` to a fresh `walletY_101`. `completeTransferCheck` evaluates `0 > 100 = false`, REJECT is not taken, `recordTransfer` runs `adjustTotalInvestorsCounts(_to, Increase)`, and `totalInvestors = 101`. The cap-encoded regulatory commitment (Reg-A Tier-2 unaccredited count, 506(b) accredited count, etc.) is silently breached; the same admission would have correctly reverted had it originated from a regular-investor wallet.

**Recommended Mitigation:** If the cap is meant to apply to platform-wallet sources, name the offset condition explicitly and invert it:

```solidity
bool senderDecrements = !isPlatformWalletFrom && _args.fromInvestorBalance == _args.value;
if (
    IDSComplianceConfigurationService(_services[COMPLIANCE_CONFIGURATION_SERVICE]).getTotalInvestorsLimit() != 0 &&
    !senderDecrements &&
    ComplianceServiceRegulated(_services[COMPLIANCE_SERVICE]).getTotalInvestorsCount() >=
    IDSComplianceConfigurationService(_services[COMPLIANCE_CONFIGURATION_SERVICE]).getTotalInvestorsLimit() &&
    isNewInvestor(toInvestorBalance)
) {
    return (40, MAX_INVESTORS_IN_CATEGORY);
}
```

The same correction shape applies to the JP, US, US-accredited, and EU retail caps, all of which use the `_args.fromInvestorBalance > _args.value` predicate and inherit the same blind spot for platform-wallet senders.

If platform-wallet sources are intended to be cap-exempt by design, document the carve-out explicitly in the function comment so a future maintainer doesn't conflate the platform-wallet case with the depleter case when refactoring.


**Securitize:** Fixed in [bf8f8de](https://github.com/securitize-io/dstoken/commit/bf8f8de99072dec3f0b0840f0178a1ff255a43b6).

**Cyfrin:** Verified.
