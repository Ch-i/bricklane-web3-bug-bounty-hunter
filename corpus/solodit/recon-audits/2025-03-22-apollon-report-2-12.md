---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-2-12
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-03-22T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md
tags:
- firm:recon-audits
- report:2025-03-22-apollon-report
title: '[M-13] Operative Risks tied to changing Risk Based Parameter'
vuln_class: []
---

# [M-13] Operative Risks tied to changing Risk Based Parameter

_Section severity (from Solodit section header): Medium_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Executive Summary**

This is a collection of operative risks that come from maintaining and updating Apollon

I highly recommend you go through this list, create your own list, and ensure that at all times these risks are considered


**Updating `setCollTokenSupportedCollateralRatio` can cause multiple economic exploits**

```solidity
  function setCollTokenSupportedCollateralRatio(
    address _collTokenAddress,
    uint _supportedCollateralRatio
  ) external override onlyOwner {
    if (_supportedCollateralRatio < MCR) revert SupportedRatioUnderMCR();
    collTokenSupportedCollateralRatio[_collTokenAddress] = _supportedCollateralRatio;
    emit CollTokenSupportedCollateralRatioSet(_collTokenAddress, _supportedCollateralRatio);
  }
```

Updating this ratio can:

- Cause Recovery Mode
- Be sandwhiched to trigger Recovery Mode
- Cause Liquidations
- Be sandwhiched to cause self-liquidations

The setter itself is not a vulnerability, however, the mechanisms around changing these risk-based values are very commonly a pre-condition to Critical Severity Exploits

The most important consideration is tied to how exactly a change in Collateral Ratio would be enacted

- Can you pause minting and borrowing?
- Can you verify that all users are solvent and will remain solvent after the change?
- Can you have a buffer that will prevent actors from having a step-wise change in their Collateralization Ratio?
- Will the governance proposal be executable by anyone?
- Will you liquidate any unhealthy position as part of the proposal?

Due to the complexity, I'm flagging this as a delicate Operational Security area, however, I will not be able to provide specific advice at this time

**`setAlternativePriceFeed` can cause liquidations, self-liquidations or insolvency and bad debt**

This change could also cause positions to go from healthy to undercollateralized

The change may also be sandwiched

More importantly, if governance changes can be broadcasted by anyone, the sandwiched will not be mitigable and would be a perfect opportunity for an economic exploit

**Gov token must be configured**

Since gov token is used as part of reserve pool, then it must be configured to have some validity as collateral

**Mitigation**

Recognize the risks tied to changing these settings and plan accordingly, do consult Security Researchers at that time
