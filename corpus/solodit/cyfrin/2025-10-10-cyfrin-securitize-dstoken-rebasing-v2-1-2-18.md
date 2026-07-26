---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-2-18
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: Platform Wallet not exception for Maximum Holdings Per Investor Limits
vuln_class: []
---

# Platform Wallet not exception for Maximum Holdings Per Investor Limits

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** The `preIssuanceCheck` function in `ComplianceServiceRegulated.sol` exhibits inconsistent behavior regarding platform wallet exemptions for investor holdings limits. While platform wallets are properly exempted from the minimum holdings per investor check, they are not exempted from the maximum holdings per investor check.

```solidity
if (
    !_args.isPlatformWalletTo &&
    toInvestorBalance + _args.value < IDSComplianceConfigurationService(_services[COMPLIANCE_CONFIGURATION_SERVICE]).getMinimumHoldingsPerInvestor()
) {
    return (51, AMOUNT_OF_TOKENS_UNDER_MIN);
}
```
The minimum holdings check correctly includes `!_args.isPlatformWalletTo &&` to exempt platform wallets, but the maximum holdings check lacks this exemption, subjecting platform wallets to the same maximum holdings limits as regular investors.

```solidity
if (
            isMaximumHoldingsPerInvestorOk(
                IDSComplianceConfigurationService(_services[COMPLIANCE_CONFIGURATION_SERVICE]).getMaximumHoldingsPerInvestor(),
                toInvestorBalance, _args.value)
        ) {
            return (52, AMOUNT_OF_TOKENS_ABOVE_MAX);
        }

```

**Impact:** Platform wallets may be unable to hold sufficient tokens for operational purposes due to maximum holdings limits.

**Recommended Mitigation:** Add platform wallet exemption to the maximum holdings check:
```diff
if (
+    !_args.isPlatformWalletTo &&
    isMaximumHoldingsPerInvestorOk(
        complianceConfigurationService.getMaximumHoldingsPerInvestor(),
        balanceOfInvestorTo,
        _value)
) {
    return (52, AMOUNT_OF_TOKENS_ABOVE_MAX);
}
```

**Securitize:** Fixed in commits [5b96460](https://github.com/securitize-io/dstoken/commit/5b964605cd92bdc1307f975355ec7ca402265119), [2cab0c2](https://github.com/securitize-io/dstoken/commit/2cab0c298cbeee8951c76e63947a69dc48a2698b).

**Cyfrin:** Verified.
