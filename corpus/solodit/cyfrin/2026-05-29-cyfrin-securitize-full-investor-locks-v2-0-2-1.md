---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-29-cyfrin-securitize-full-investor-locks-v2-0-2-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-05-29T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-29-cyfrin-securitize-full-investor-locks-v2-0
title: '`ComplianceServiceLibrary::completeTransferCheck` reallocation short-circuit
  precedes the FORBIDDEN-destination check'
vuln_class: []
---

# `ComplianceServiceLibrary::completeTransferCheck` reallocation short-circuit precedes the FORBIDDEN-destination check

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md)_

---

**Description:** `ComplianceServiceLibrary::completeTransferCheck` at `contracts/compliance/ComplianceServiceRegulated.sol:252-256` short-circuits with `(0, VALID)` when both endpoints of a transfer resolve to the same investor id (the reallocation case). The short-circuit is placed before the FORBIDDEN-destination check at line 268, so when an investor's country is mapped to FORBIDDEN, transfers between two of their own wallets bypass the FORBIDDEN check, while transfers to third-party wallets correctly fail the reallocation predicate and hit the FORBIDDEN gate downstream. The gap is specifically `FORBIDDEN region + not fully locked + same-investor reallocation`.

**Files:**

`ComplianceServiceLibrary::completeTransferCheck`

**Recommended Mitigation:** Add a region predicate to the reallocation short-circuit, or hoist the FORBIDDEN check above it:

```solidity
uint256 toRegion = getCountryCompliance(_services, _args.to);
if (
    !CommonUtils.isEmptyString(investorFrom) &&
    CommonUtils.isEqualString(investorFrom, investorTo) &&
    toRegion != FORBIDDEN &&
    _args.fromRegion != FORBIDDEN
) {
    return (0, VALID);
}

if (toRegion == FORBIDDEN) {
    return (26, DESTINATION_RESTRICTED);
}
```


**Securitize:** Acknowledged.
