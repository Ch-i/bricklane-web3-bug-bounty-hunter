---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-29-cyfrin-securitize-full-investor-locks-v2-0-1-4
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
title: '`ComplianceServiceRegulated::preIssuanceCheck` missing platform-wallet short-circuit
  spuriously rejects treasury funding'
vuln_class: []
---

# `ComplianceServiceRegulated::preIssuanceCheck` missing platform-wallet short-circuit spuriously rejects treasury funding

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md)_

---

**Description:** `ComplianceServiceLibrary::doPreTransferCheckRegulated` short-circuits with `(0, VALID)` when the recipient is a platform wallet (lines 228-238), exempting platform-wallet destinations from cap and region checks. Platform-wallet recipients are not counted in `totalInvestors`: `adjustTotalInvestorsCounts` at line 673 guards on `!isSpecialWallet(_wallet)`, so the increment never fires for a platform-wallet recipient even if the function is called.

`ComplianceServiceLibrary::preIssuanceCheck` at contracts/compliance/ComplianceServiceRegulated.sol:446-570 does NOT have a symmetric short-circuit. It checks `isPlatformWallet = isPlatformWallet(_to)` at line 525 and uses the flag only to skip the regional MIN/MAX holdings checks (lines 536, 544, 553, 560). The earlier cap gates fire regardless:

- `getForceAccredited()` at line 472-477 - fires when the flag is true and `isAccreditedTo == false`. A platform wallet has no investor record, so `isAccredited(_services, _to)` returns `isAccreditedInvestor("") == false`. When the issuer turns on `forceAccredited`, every issuance to a platform wallet is rejected with `(61, ONLY_ACCREDITED)`.
- `getNonAccreditedInvestorsLimit()` at lines 480-489 - fires inside `isNewInvestor(balanceOfInvestorTo)` (balance 0 for the empty-investor) when `!isAccreditedTo`. When the non-accredited limit is reached, every issuance to a platform wallet is rejected with `(40, MAX_INVESTORS_IN_CATEGORY)` even though the issuance does not actually onboard a new investor: `recordIssuance` calls `adjustTotalInvestorsCounts(platformWallet, Increase)`, but the `!isSpecialWallet(_wallet)` guard at `ComplianceServiceRegulated.sol:673` short-circuits before the `totalInvestors++`, so the counter stays unchanged.
- `getTotalInvestorsLimit()` at lines 491-496 - fires when the cap is reached and `isNewInvestor(balanceOfInvestorTo)` is true. Same shape: platform-wallet issuance is structurally not a new-investor admission, but `preIssuanceCheck` blocks it as if it were.

**Files:**

`ComplianceServiceLibrary::preIssuanceCheck, doPreTransferCheckRegulated`

**Impact:** Routine issuer treasury funding via direct issuance to a platform wallet (custody account, redemption pool, DeFi pool integration) is spuriously rejected whenever any of the three pre-check cap gates is reached: `(61, ONLY_ACCREDITED)` under `forceAccredited`, `(40, MAX_INVESTORS_IN_CATEGORY)` when `totalInvestorsCount >= totalInvestorsLimit`, and the same error against the non-accredited subcount. BC-1779 deepens the asymmetry between `preIssuanceCheck` and `doPreTransferCheckRegulated`: the new lock-check block at lines 205-223 is gated on `!isPlatformWallet(_from)`, exempting platform-wallet senders from the new enforcement entirely, while `preIssuanceCheck` continues to fire its caps against platform-wallet recipients. Admin can work around each rejection: bump the relevant cap by one via `setTotalInvestorsLimit(currentLimit + 1)` (or the sibling setters for the non-accredited and US/JP/EU caps that share the same predicate shape), toggle `setForceAccredited(false)` for the accredited gate, then fund the treasury, then restore the original config. Each workaround temporarily relaxes a compliance gate for the funding window.

**Recommended Mitigation:** Add a platform-wallet short-circuit at the top of `preIssuanceCheck` mirroring the one in `doPreTransferCheckRegulated`:

```solidity
function preIssuanceCheck(address[] calldata _services, address _to, uint256 _value) public view returns (uint256 code, string memory reason) {
    ComplianceServiceRegulated complianceService = ComplianceServiceRegulated(_services[COMPLIANCE_SERVICE]);

    if (!complianceService.checkWhitelisted(_to)) {
        return (20, WALLET_NOT_IN_REGISTRY_SERVICE);
    }

    if (IDSWalletManager(_services[WALLET_MANAGER]).isPlatformWallet(_to)) {
        return (0, VALID);
    }

    IDSComplianceConfigurationService complianceConfigurationService = IDSComplianceConfigurationService(_services[COMPLIANCE_CONFIGURATION_SERVICE]);
    ...
}
```

The short-circuit position comes after `checkWhitelisted` (because the whitelist gate still applies to platform wallets - `ComplianceServiceWhitelisted::checkWhitelisted` exempts them, but maintaining the call site preserves the dispatch order). The early-return then skips all the cap/force gates that should not apply to platform-wallet destinations, matching the structural exemption that `doPreTransferCheckRegulated` already encodes.


**Securitize:** Fixed in [752accf](https://github.com/securitize-io/dstoken/commit/752accffcc1aa40bba152ea319dfcf23918d8134).

**Cyfrin:** Verified.
