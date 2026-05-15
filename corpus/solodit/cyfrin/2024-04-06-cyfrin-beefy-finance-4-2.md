---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-4-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-04-06T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md
tags:
- firm:cyfrin
- report:2024-04-06-cyfrin-beefy-finance
title: Cache array length outside of loops and consider unchecked loop incrementing
vuln_class: []
---

# Cache array length outside of loops and consider unchecked loop incrementing

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-06-cyfrin-beefy-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md)_

---

**Description:** Cache array length outside of loops and consider using `unchecked {++i;}` if not compiling with `solc --ir-optimized --optimize`:

File: `BeefyQIVault.sol`
```solidity
210:                for (uint i; i < rewardTokens.length; ++i) {
216:                                        for (uint j; j < reward.assets.length - 1;) {
358:                        for (uint i; i < _swapInfo.length; ++i) {
370:                for (uint256 i; i < rewardTokens.length; ++i) {
```

**Beefy:**
Acknowledged.
