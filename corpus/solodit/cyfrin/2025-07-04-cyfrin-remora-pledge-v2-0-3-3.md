---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-3-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: Using explicit unsigned integer sizing instead of `uint`
vuln_class: []
---

# Using explicit unsigned integer sizing instead of `uint`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** In Solidity `uint` automatically maps to `uint256` but it is considered good practice to specify the exact size when declaring variables:
```solidity
PaymentSettler.sol
124:        for (uint i = 0; i < len; ++i) {
174:        for (uint i = 0; i < tokens.length; ++i) {
227:        for (uint i = 0; i < tokenList.length; ++i) {

RWAToken/DocumentManager.sol
224:        for (uint i = 0; i < dHLen; ++i) {

TokenBank.sol
185:        for (uint i = 0; i < len; ++i) {
260:        for (uint i = 0; i < developments.length; ++i)
267:        for (uint i = 0; i < developments.length; ++i) {
```

**Remora:** Fixed in commit [6602423](https://github.com/remora-projects/remora-smart-contracts/commit/66024232cfea24b69bd055086f8088d40f3d1d4a).

**Cyfrin:** Verified.
