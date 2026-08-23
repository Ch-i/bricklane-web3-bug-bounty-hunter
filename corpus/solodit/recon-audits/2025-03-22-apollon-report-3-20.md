---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-3-20
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-03-22T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md
tags:
- firm:recon-audits
- report:2025-03-22-apollon-report
title: '[L-21] `SwapPair.getSwapFee` charges for crossing the middle price'
vuln_class: []
---

# [L-21] `SwapPair.getSwapFee` charges for crossing the middle price

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Impact**

`getSwapFee` computes the fee to be paid as follows:

https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/SwapPair.sol#L196-L199

```solidity
      if ( /// @audit No deviation threshold | Spot vs Oracle
        (postDexPrice > oraclePrice && postDexPrice > preDexPrice) || /// @audit Logical mechanism of swapping?
        (postDexPrice < oraclePrice && preDexPrice > postDexPrice)
      ) {
```

We can chart out the logic as follows:

- Post  > Oracle
- Post > Prev > Oracle
- Post > Oracle > Prev

- Post < Oracle
- Post < Prev < Oracle 
- Post < Oracle < Prev

Meaning this is charging a fee whenever the absolute postDexPrice surpasses the absolute oracle price

So when crossing the impact is "halved"

When not crossing the middle price, the average between the two dex prices will be very distant from the oracle price, causing the fee to be higher, whereas when crossing the fee would effectively be halved

**Mitigation**

I don't believe there's any need for a specific mitigation
