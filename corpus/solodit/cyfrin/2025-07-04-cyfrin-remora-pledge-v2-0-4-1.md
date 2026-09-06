---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-4-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: Don't initialize to default values
vuln_class: []
---

# Don't initialize to default values

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** Don't initialize to default values:
```solidity
RWAToken/DividendManager.sol
186:      $._currentPayoutIndex = 0;

RWAToken/DocumentManager.sol
118:        for (uint256 i = 0; i < numDocs; ++i) {
222:        for (uint i = 0; i < dHLen; ++i) {

RWAToken/DividendManager.sol
349:                for (uint256 i = 0; i < len; ++i) {
463:        for (uint256 i = 0; i < rHolderStatus.forwardedPayouts.length; ++i) {

TokenBank.sol
152:        for (uint i = 0; i < developments.length; ++i) {
225:        uint64 totalValue = 0;
226:        for (uint i = 0; i < developments.length; ++i)
232:        uint64 totalValue = 0;
233:        for (uint i = 0; i < developments.length; ++i) {

PledgeManager.sol
119:        tokensSold = 0;
278:        uint256 fee = 0;

RemoraIntermediary.sol
258:        for (uint256 i = 0; i < len; ++i) {

PaymentSettler.sol
124:        for (uint i = 0; i < len; ++i) {
174:        for (uint i = 0; i < tokens.length; ++i) {
226:        uint256 totalFees = 0;
227:        for (uint i = 0; i < tokenList.length; ++i) {
```

**Remora:** Fixed in commit [6602423](https://github.com/remora-projects/remora-smart-contracts/commit/66024232cfea24b69bd055086f8088d40f3d1d4a).

**Cyfrin:** Verified.
