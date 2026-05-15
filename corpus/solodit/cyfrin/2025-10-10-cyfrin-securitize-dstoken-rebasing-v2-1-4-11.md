---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-4-11
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: Cache computation results instead of repeatedly performing the same computation
vuln_class: []
---

# Cache computation results instead of repeatedly performing the same computation

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** Cache computation results instead of repeatedly performing the same computation.

* `contracts/utils/TransactionRelayer.sol`
```solidity
// cache `toBytes32(investorId)` in `setInvestorNonce`
142:        uint256 investorNonce = noncePerInvestor[toBytes32(investorId)];
144:        noncePerInvestor[toBytes32(investorId)] = newNonce;

// cache `toBytes32(senderInvestor)` in `doExecuteByInvestor`
175:                        noncePerInvestor[toBytes32(senderInvestor)],
178:                        keccak256(abi.encodePacked(senderInvestor)),
190:        noncePerInvestor[toBytes32(senderInvestor)]++;
```

**Securitize:** Acknowledged.
