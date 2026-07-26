---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-3-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-03-22T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md
tags:
- firm:recon-audits
- report:2025-03-22-apollon-report
title: '[L-03] `massUpdatePools` needs to be capped due to OOG reverts'
vuln_class: []
---

# [L-03] `massUpdatePools` needs to be capped due to OOG reverts

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Impact**

`massUpdatePools` looks as follows:

```solidity
 function massUpdatePools() public {
    uint length = pools.length;
    for (uint n = 0; n < length; n++) {
      updatePool(pools[n]);
    }
  }
```

Meaning it will iterate over all known pools

The gas limit on SEI is 10MLN gas per block

Assuming around 25k gas per update, that's 400 pools before the function reverts

I just did some quick napkin math on the amount of storage slots used, you should write a test to verify the limit as to avoid getting reverts in prod

That said, anything below 100 pools will have a high margin of safety

**Mitigation**

Ensure you do not surpass 100 pools as to avoid consuming too much gas which could cause reverts
