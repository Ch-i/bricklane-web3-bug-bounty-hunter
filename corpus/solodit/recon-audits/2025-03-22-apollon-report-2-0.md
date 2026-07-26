---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-2-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-03-22T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md
tags:
- firm:recon-audits
- report:2025-03-22-apollon-report
title: '[M-01] `RedemptionOperations` Redemptions should be disabled during Recovery
  Mode'
vuln_class: []
---

# [M-01] `RedemptionOperations` Redemptions should be disabled during Recovery Mode

_Section severity (from Solodit section header): Medium_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Impact**

`RedemptionOperations` checks the `TCR < MCR`, but should most likely check for `TCR < CCR`

https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/RedemptionOperations.sol#L101-L103

```solidity
    (, uint TCR, , ) = storagePool.checkRecoveryMode(vars.priceCache); /// @audit High? not checking RM -> Mint for free, Inflate total supply (pay no redemption), redeem at small fee
    if (TCR < MCR) revert LessThanMCR(); /// @audit-ok force to liquidate if all system is insolvent

```

This is because during Recovery Mode, minting fees are voided, meaning that the system may open up to additional arbitrages via Redemptions

Redemptions are generally disabled during RM in favour of liquidations


**Mitigation**

Investigate if additional arbitrages could be detrimental to your protocol due to reduced minting fees

From checking liquity they use a check similar to yours:
https://github.com/liquity/dev/blob/e38edf3dd67e5ca7e38b83bcf32d515f896a7d2f/packages/contracts/contracts/TroveManager.sol#L948-L962
