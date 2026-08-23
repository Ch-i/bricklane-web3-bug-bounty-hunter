---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-02-cyfrin-evo-soulboundtoken-v2-0-1-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-06-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-02-cyfrin-evo-soulboundtoken-v2.0.md
tags:
- firm:cyfrin
- report:2025-06-02-cyfrin-evo-soulboundtoken-v2-0
title: Don't initialize to default values
vuln_class: []
---

# Don't initialize to default values

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-02-cyfrin-evo-soulboundtoken-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-02-cyfrin-evo-soulboundtoken-v2.0.md)_

---

**Description:** Don't initialize to default values as Solidity already does this:
```solidity
SoulBoundToken.sol
125:        for (uint256 i = 0; i < admins.length; ++i) {
162:        for (uint256 i = 0; i < accounts.length; ++i) {
226:        for (uint256 i = 0; i < accounts.length; ++i) {
245:        for (uint256 i = 0; i < accounts.length; ++i) {
270:        for (uint256 i = 0; i < accounts.length; ++i) {
289:        for (uint256 i = 0; i < accounts.length; ++i) {
312:        for (uint256 i = 0; i < accounts.length; ++i) {
```

**Evo:**
Fixed in commit [f594ae0](https://github.com/contractlevel/sbt/commit/f594ae004d4afc80f19e17c0f61d50caa00a4811).

**Cyfrin:** Verified.
