---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-3-18
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-03-22T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md
tags:
- firm:recon-audits
- report:2025-03-22-apollon-report
title: '[L-19] `RedeptionOperations.checkValidRedemptionHint` check should use `>=`'
vuln_class: []
---

# [L-19] `RedeptionOperations.checkValidRedemptionHint` check should use `>=`

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Impact**

The check in `checkValidRedemptionHint` for the current hint is as follows:

https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/RedemptionOperations.sol#L212

```solidity
if (hintCR < hintIMCR) revert HintBelowMCR(); // should be liquidated, not redeemed from
```

Which asserts that the hint is not liquidatable outside of recovery mode (which is checked in `redeemCollateral`)

The check below is to ensure that the trove being redeemed is the riskiest trove that is not underwater

https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/RedemptionOperations.sol#L217-L218

```solidity
    if (nextTrove != address(0) && nextTroveCR > nextTroveMCR) revert InvalidHintLowerCRExists(); /// @audit TO CHECK

```

The check is the opposite of the above, therefore the comparison: `nextTroveCR > nextTroveMCR` should be `nextTroveCR >= nextTroveMCR`

**Mitigation**

Change `nextTroveCR > nextTroveMCR` to `nextTroveCR >= nextTroveMCR`
