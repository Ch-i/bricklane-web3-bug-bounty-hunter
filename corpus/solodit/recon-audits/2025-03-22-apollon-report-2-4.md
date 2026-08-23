---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-2-4
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-03-22T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md
tags:
- firm:recon-audits
- report:2025-03-22-apollon-report
title: '[M-05] Decay Coefficient could round down and have an effective slower decay'
vuln_class: []
---

# [M-05] Decay Coefficient could round down and have an effective slower decay

_Section severity (from Solodit section header): Medium_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Impact**

`calcDecayedStableCoinBaseRate` calls `_minutesPassedSinceLastFeeOp` which rounds down by up to 1 minute - 1

https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/TroveManager.sol#L987-L997

```solidity
  function calcDecayedStableCoinBaseRate() public view override returns (uint) {
    uint minutesPassed = _minutesPassedSinceLastFeeOp();
    uint decayFactor = LiquityMath._decPow(MINUTE_DECAY_FACTOR, minutesPassed);

    return (stableCoinBaseRate * decayFactor) / DECIMAL_PRECISION;
  }

  function _minutesPassedSinceLastFeeOp() internal view returns (uint) {
    return (block.timestamp - lastFeeOperationTime) / 1 minutes;
  }

```

This, in conjunction with the logic `_updateLastFeeOpTime`

https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/TroveManager.sol#L980-L984

```solidity
    uint timePassed = block.timestamp - lastFeeOperationTime;
    if (timePassed >= 1 minutes) { /// @audit Can we abuse this in some way? | See ETHOS and eBTC findings
      lastFeeOperationTime = block.timestamp;
      emit LastFeeOpTimeUpdated(block.timestamp);
    }
```

will make the decay factor decay slower than intended

This finding was found in the ETHOS contest by Chaduke:
https://github.com/code-423n4/2023-02-ethos-findings/issues/33
