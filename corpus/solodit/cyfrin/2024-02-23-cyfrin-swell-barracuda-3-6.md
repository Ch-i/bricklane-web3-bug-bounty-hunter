---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-02-23-cyfrin-swell-barracuda-3-6
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-02-23T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md
tags:
- firm:cyfrin
- report:2024-02-23-cyfrin-swell-barracuda
title: Use constant for unchanging deposit amount
vuln_class: []
---

# Use constant for unchanging deposit amount

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-02-23-cyfrin-swell-barracuda.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md)_

---

**Description:** In `DepositManager::setupValidators` there is no use in paying gas to declare then later read this variable which never changes:
```solidity
uint256 depositAmount = 32 ether;
```

Rather simply define a constant:
```solidity
uint256 private constant DEPOSIT_AMOUNT = 32 ether;
```
And use that constant instead.

**Swell:** Acknowledged.

\clearpage
