---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-28-cyfrin-rocko-refinance-v2-0-1-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-03-28T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-28-cyfrin-rocko-refinance-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-28-cyfrin-rocko-refinance-v2-0
title: Events missing indexed parameters
vuln_class: []
---

# Events missing indexed parameters

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-28-cyfrin-rocko-refinance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-28-cyfrin-rocko-refinance-v2.0.md)_

---

**Description:** Events in Solidity can have up to three indexed parameters, which are stored as topics in the event log. Indexed parameters allow for efficient filtering and searching of events by off-chain services. Without indexed parameters, it becomes more difficult and resource-intensive for applications to filter for specific events.

There are instances of events missing indexed parameters that could be improved.
```solidity
    event LogRefinanceLoanCall(
        string logType,
        address rockoWallet,
        string from,
        string to,
        uint256 debtBalance,
        address debtTokenAddress,
        address collateralTokenAddress,
        address aCollateralTokenAddress,
        Id morphoMarketId
    );
    event LogFlashLoanCallback(
        string logType,
        address rockoWallet,
        string from,
        string to,
        address debtTokenAddress,
        address collateralTokenAddress,
        address aCollateralTokenAddress,
        uint256 flashBorrowAmount,
        bytes data,
        Id morphoMarketId
    );
```

**Recommended Mitigation:** Add the `indexed` keyword to important parameters in the event that would commonly be used for filtering, such as `rockoWallet`, `debtTokenAddress`, and `collateralTokenAddress`.

**Rocko:** Fixed in commit [f5c9c80](https://github.com/getrocko/onchain/commit/f5c9c8051d5ba1bf04774ae6e8aa407aeddbcde1).

**Cyfrin:** Verified.
