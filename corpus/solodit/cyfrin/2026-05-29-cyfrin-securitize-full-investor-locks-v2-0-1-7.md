---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-29-cyfrin-securitize-full-investor-locks-v2-0-1-7
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
title: '`ComplianceServiceLibrary::getUSInvestorsLimit` floor-zero leak and `preIssuanceCheck`
  raw-cap read fragment US-investor cap enforcement'
vuln_class: []
---

# `ComplianceServiceLibrary::getUSInvestorsLimit` floor-zero leak and `preIssuanceCheck` raw-cap read fragment US-investor cap enforcement

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md)_

---

**Description:** The US-investor cap is enforced at two sites: at issuance time inside `preIssuanceCheck`, and at transfer time inside `completeTransferCheck`. Both sites consult the same configured values: an absolute integer cap (`getUSInvestorsLimit()`) and a percentage-of-total cap (`maxUSInvestorsPercentage`). Two independent gaps along this enforcement surface combine to silently defeat the cap at small totals or percentage-only configurations.

**Component 1: `ComplianceServiceLibrary::getUSInvestorsLimit` floor-division bootstrap-zero.** The library helper at lines 119-132 combines the absolute and percentage caps using `Math.min`:

```solidity
function getUSInvestorsLimit(address[] memory _services) internal view returns (uint256) {
    if (maxPercentage == 0)   return staticLimit;
    if (staticLimit == 0)     return maxPercentage * totalInvestors / 100;
    return Math.min(staticLimit, maxPercentage * totalInvestors / 100);
}
```

The percentage leg uses integer floor-division. Whenever `maxPercentage * totalInvestors < 100`, the floor result is `0`. The downstream consumer in `completeTransferCheck` at lines 365-372 guards with `usInvestorsLimit != 0` and reads a `0` return as "no cap configured," skipping the cap entirely:

```solidity
uint256 usInvestorsLimit = getUSInvestorsLimit(_services);
if (
    usInvestorsLimit != 0 &&                         // <-- read as "no cap configured"
    (_args.fromRegion != US || _args.fromInvestorBalance > _args.value) &&
    getUSInvestorsCount() >= usInvestorsLimit &&
    isNewInvestor(toInvestorBalance)
) {
    return (40, MAX_INVESTORS_IN_CATEGORY);
}
```

The cap is therefore silently disabled while `totalInvestors < ceil(100 / maxPercentage)`. For typical Reg-D-style percentage settings of 1-10%, the bootstrap window covers the first ten to one hundred investors of the deployment. The sub-case where the operator sets BOTH a static cap (intended as a hard ceiling) AND a percentage cap (intended as a soft constraint) is particularly bad: `Math.min(staticLimit, 0) = 0` defeats the static cap entirely, not just the percentage leg.

**Component 2: `preIssuanceCheck` reads the raw absolute cap instead of the library helper.** The issuance-time consumer at line 500 does NOT call `getUSInvestorsLimit`; it reads the raw absolute cap directly:

```solidity
uint256 limit = complianceConfigurationService.getUSInvestorsLimit();
if (limit != 0 && newUSInvestorsCount > limit) { ... }
```

The two enforcement sites therefore disagree on what "the US-investor cap" means. If the operator configures only the percentage cap (leaving the absolute cap at 0), `preIssuanceCheck` reads the raw absolute cap as "unconfigured" and skips the cap entirely on the issuance path. The transfer path's library helper still computes the percentage cap (subject to Component 1's bootstrap-zero) and enforces it.

**Files:**

- `contracts/compliance/ComplianceServiceRegulated.sol` (`getUSInvestorsLimit` lines 119-132; `completeTransferCheck` consumer at line 365-372; `preIssuanceCheck` raw read at line 500)

**Impact:** Two failure modes, and a compound mode when both apply:

- **Bootstrap window (Component 1 alone):** with both static and percentage caps configured, the transfer-path cap is silently disabled until `totalInvestors >= ceil(100 / maxPercentage)`. For percentage settings in the typical 1-10% range, this admits 10-100 US investors before the cap engages. After the threshold the cap behaves correctly, but US investors already admitted during the bootstrap window persist.

- **Percentage-only configuration (Component 2 alone):** the issuance path skips the cap entirely. Issuances to US investors that should be blocked by the percentage cap proceed; transfers between existing investors continue to honor the cap via the library helper. The operationally visible shape is that issuances drift the US-investor count above the configured percentage cap while same-existing-population transfers stay correctly gated.

- **Compound (both apply):** with a percentage-only configuration at small totals, both lanes silently admit US investors. Self-recoverable by configuring the absolute cap as a floor, but the operator may not notice the discrepancy until a regulatory review of fresh issuances reveals US-investor counts above the configured constraints.

**Recommended Mitigation:** Two fixes are required, one per component:

- **Component 1**: change `getUSInvestorsLimit` so floor-zero cannot escape. Either guard the percentage leg with `max(1, percentageLimit)` when `maxPercentage > 0`, or restructure to return the static cap when the percentage leg would round to zero. Independently, change the consumer guard at `completeTransferCheck:367` to distinguish "unset" from "computes to zero": treat the cap as configured when either input is non-zero, and consult `getUSInvestorsLimit` only when at least one is set.

- **Component 2**: replace the raw configuration read at `preIssuanceCheck:500` with the library helper:

```solidity
uint256 limit = ComplianceServiceLibrary.getUSInvestorsLimit(_services);
```

That aligns both lanes on the same cap-resolution semantics. The Component 1 fix should land first or simultaneously, otherwise routing `preIssuanceCheck` through the buggy library helper would propagate the bootstrap-zero issue to the issuance path as well.


**Securitize:** Acknowledged.
