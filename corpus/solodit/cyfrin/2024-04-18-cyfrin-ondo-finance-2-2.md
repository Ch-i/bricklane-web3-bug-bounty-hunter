---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-18-cyfrin-ondo-finance-2-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-04-18T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md
tags:
- firm:cyfrin
- report:2024-04-18-cyfrin-ondo-finance
title: Avoid unnecessary initialization to zero
vuln_class: []
---

# Avoid unnecessary initialization to zero

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-18-cyfrin-ondo-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md)_

---

**Description:** Avoid unnecessary initialization to zero:
```solidity
File: contracts/ousg/InvestorBasedRateLimiter.sol

253:     for (uint256 i = 0; i < addresses.length; ++i) {
```

```solidity
File: contracts/ousg/ousgInstantManager.sol

106:   uint256 public mintFee = 0;

109:   uint256 public redeemFee = 0;

881:     for (uint256 i = 0; i < exCallData.length; ++i) {
```

**Ondo:**
Fixed in commit [a7dab64](https://github.com/ondoprotocol/rwa-internal/commit/a7dab64a2ad87b6ca051c3aeb5371c8f9f933350).

**Cyfrin:** Verified.
