---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-3-6
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: Use named constants instead of hard-coded literals for important values
vuln_class: []
---

# Use named constants instead of hard-coded literals for important values

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** Use named constants instead of hard-coded literals for important values:
```solidity
contracts/compliance/ComplianceServiceRegulated.sol
// error codes in `ComplianceServiceRegulated::completeTransferCheck`
217:            return (0, VALID);
221:            return (90, INVESTOR_LIQUIDATE_ONLY);
225:            return (20, WALLET_NOT_IN_REGISTRY_SERVICE);
230:            return (26, DESTINATION_RESTRICTED);
238:            return (16, TOKENS_LOCKED);
243:                return (32, HOLD_UP);
250:                return (51, AMOUNT_OF_TOKENS_UNDER_MIN);
257:                return (50, ONLY_FULL_TRANSFER);
261:                return (33, HOLD_UP);
269:                return (25, FLOWBACK);
276:                return (50, ONLY_FULL_TRANSFER);
286:                return (51, AMOUNT_OF_TOKENS_UNDER_MIN);
294:            return (61, ONLY_ACCREDITED);
305:                return (40, MAX_INVESTORS_IN_CATEGORY);
316:                return (40, MAX_INVESTORS_IN_CATEGORY);
322:                return (51, AMOUNT_OF_TOKENS_UNDER_MIN);
329:                return (62, ONLY_US_ACCREDITED);
339:                return (40, MAX_INVESTORS_IN_CATEGORY);
350:                return (40, MAX_INVESTORS_IN_CATEGORY);
356:                return (51, AMOUNT_OF_TOKENS_UNDER_MIN);
362:                return (40, MAX_INVESTORS_IN_CATEGORY);
373:            return (40, MAX_INVESTORS_IN_CATEGORY);
382:            return (71, NOT_ENOUGH_INVESTORS);
390:            return (51, AMOUNT_OF_TOKENS_UNDER_MIN);
397:            return (51, AMOUNT_OF_TOKENS_UNDER_MIN);
405:            return (52, AMOUNT_OF_TOKENS_ABOVE_MAX);
408:        return (0, VALID);

// denominator representing 100%
108:            return compConfService.getMaxUSInvestorsPercentage() * (complianceService.getTotalInvestorsCount()) / 100;
111:        return Math.min(compConfService.getUSInvestorsLimit(), compConfService.getMaxUSInvestorsPercentage() * (complianceService.getTotalInvestorsCount()) / 100);

compliance/ComplianceConfigurationService.sol
238:        require(_uint_values.length == 16, "Wrong length of parameters");

registry/RegistryService.sol
43:        for (uint8 index = 0; index < 16; index++) {
135:        require(_attributeId < 16, "Unknown attribute");

trust/TrustService.sol
216:        require(_addresses.length <= 30, "Exceeded the maximum number of addresses");

compliance/WalletManager.sol
74:        require(_wallets.length <= 30, "Exceeded the maximum number of wallets");
96:        require(_wallets.length <= 30, "Exceeded the maximum number of wallets");
```

**Securitize:** Acknowledged.
