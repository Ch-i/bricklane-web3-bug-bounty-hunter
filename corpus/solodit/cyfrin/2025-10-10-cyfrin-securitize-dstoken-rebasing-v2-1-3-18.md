---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-3-18
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: Using `block.number` instead of `block.timestamp` as an expiration check to
  execute signature
vuln_class: []
---

# Using `block.number` instead of `block.timestamp` as an expiration check to execute signature

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

Description:
On `TransactionRelayer::executeByInvestorWithBlockLimit()`, the 3rd value in the `params` array is compared against the `block.number`, the purpose is to prevent executing old signatures. Using `block.number` is not recommended when enforcing time-dependent operations.

```solidity
    function executeByInvestorWithBlockLimit(
        ...
        uint256[] memory params
    ) public {
        ...
        require(params[2] >= block.number, "Transaction too old");
        ...
    }

```

It is best to use `block.timestamp` because the `block.number` time length varies from chain to chain.

Securitize:

Cyfrin:
