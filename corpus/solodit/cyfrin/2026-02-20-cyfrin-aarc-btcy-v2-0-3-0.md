---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-20-cyfrin-aarc-btcy-v2-0-3-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-02-20T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-20-cyfrin-aarc-btcy-v2-0
title: In Solidity don't initialize to default values
vuln_class: []
---

# In Solidity don't initialize to default values

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-20-cyfrin-aarc-btcy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md)_

---

**Description:** In Solidity don't initialize to default values:
```solidity
DepositWithdraw.sol
200:        for (uint256 i = 0; i < users.length; i++) {
213:        for (uint256 i = 0; i < users.length; i++) {

IBTCYHub.sol
163:        $.instantRedemptionFee = 0; // 0%
164:        $.regularRedemptionFee = 0; // 0%
165:        $.instantSubscriptionFee = 0; // 0%
166:        $.regularSubscriptionFee = 0; // 0%
352:        for (uint256 i = 0; i < data.depositIds.length;) {
498:        for (uint256 i = 0; i < data.redemptionIds.length;) {

Pricer.sol
210:        for (uint256 i = 0; i < _priceIds.length;) {

BTCY.sol
178:        for (uint256 i = 0; i < accounts.length; i++) {

base/AllowList.sol
69:        for (uint256 i = 0; i < accounts.length; ++i) {
98:        for (uint256 i = 0; i < accounts.length; ++i) {
```

**Aarc:** Fixed in commit [61ec34d](https://github.com/aarc-xyz/btcy-contracts-main/commit/61ec34d124bb34563b358c0f76d58d973f3ec293).

**Cyfrin:** Verified.
