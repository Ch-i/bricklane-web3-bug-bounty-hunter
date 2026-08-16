---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-27-cyfrin-majority-protocol-v2-0-5-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-01-27T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-27-cyfrin-majority-protocol-v2-0
title: In Solidity don't initialize to default values
vuln_class: []
---

# In Solidity don't initialize to default values

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-27-cyfrin-majority-protocol-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md)_

---

**Description:** In Solidity don't initialize to default values:
```solidity
session/DefaultSession.sol
125:        for (uint256 i = 0; i < questionIds.length; ++i) {
172:        for (uint256 i = 0; i < assertion.winners.length; ++i) {
174:            for (uint256 j = 0; j < questionIds.length; ++j) {

QuestionManager.sol
50:        for (uint256 i = 0; i < _questionHashes.length; i++) {

SessionManager.sol
154:    bool public livenessRequired = false;
159:    bool public creationSunsetted = false;
248:        for (uint256 i = 0; i < _promptStrategies.length; i++) {
366:        for (uint256 i = 0; i < questionIds.length; i++) {
438:        for (uint256 i = 0; i < questions.length; i++) {
474:        for (uint256 i = 0; i < questions.length; i++) {
549:        for (uint256 i = 0; i < _gameIds.length; i++) {

prompt/TriviaChoicePrompt.sol
108:        for (uint256 i = 0; i < questionIds.length; i++) {

offchain/uma/SessionResultAsserter.sol
121:        for (uint256 i = 0; i < addresses.length; i++) {
133:        for (uint256 i = 0; i < data.length; i++) {

reward/ProportionalToXPReward.sol
44:        for (uint256 i = 0; i < winners.length; ++i) {
50:        for (uint256 i = 0; i < winners.length; ++i) {
65:        for (uint256 i = 0; i < winners.length; ++i) {

reward/FixedRanksReward.sol
57:        uint256 totalPoints = 0;
58:        for (uint256 i = 0; i < _rankedRewards.length; ++i) {
76:        for (uint256 i = 0; i < winners.length; ++i) {
```

**Majestic Games:**
Fixed in commit [6686df5](https://github.com/Engage-Protocol/engage-protocol/commit/6686df583945b33ab7ab2ad64e432c0395fabeb4).

**Cyfrin:** Verified.
