---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-18-cyfrin-ondo-finance-2-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-04-18T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md
tags:
- firm:cyfrin
- report:2024-04-18-cyfrin-ondo-finance
title: Cache storage variables in stack when read multiple times without being changed
vuln_class: []
---

# Cache storage variables in stack when read multiple times without being changed

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-18-cyfrin-ondo-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md)_

---

**Description:** Reading from storage is considerably more expensive than reading from the stack so cache storage variables when read multiple times without being changed:

```solidity
File: contracts/ousg/InvestorBasedRateLimiter.sol

// @audit cache these then use cache values when emitting event to save 2 storage reads
324:      --investorAddressCount[previousInvestorId];
335:      ++investorAddressCount[newInvestorId];

// @audit cache and use cached value for check in L470 to save 1 storage read
462:    if (mintState.lastResetTime == 0) {

// @audit cache and use cached value for check in L506 to save 1 storage read
498:    if (redemptionState.lastResetTime == 0) {
```

**Ondo:**
Acknowledged.
