---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-13-cyfrin-safe-harbor-v2-0-2-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-01-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-13-cyfrin-safe-harbor-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-13-cyfrin-safe-harbor-v2-0
title: In Solidity don't initialize to default values
vuln_class: []
---

# In Solidity don't initialize to default values

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-13-cyfrin-safe-harbor-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-13-cyfrin-safe-harbor-v2.0.md)_

---

**Description:** In Solidity don't initialize to default values:
```solidity
Agreement.sol
95:        for (uint256 i = 0; i < _contactDetails.length; i++) {
105:        for (uint256 i = 0; i < _chains.length; i++) {
114:            for (uint256 j = 0; j < _chains[i].accounts.length; j++) {
125:        for (uint256 i = 0; i < _chains.length; i++) {
137:            for (uint256 j = 0; j < _chains[i].accounts.length; j++) {
149:        for (uint256 i = 0; i < _chains.length; i++) {
158:            for (uint256 j = 0; j < _chains[i].accounts.length; j++) {
169:        for (uint256 i = 0; i < _caip2ChainIds.length; i++) {
192:        for (uint256 i = 0; i < _accounts.length; i++) {
207:        for (uint256 i = 0; i < _accountAddresses.length; i++) {
235:        for (uint256 i = 0; i < _details.contactDetails.length; ++i) {
241:        for (uint256 i = 0; i < _details.chains.length; ++i) {
247:            for (uint256 j = 0; j < _details.chains[i].accounts.length; ++j) {
257:        for (uint256 i = 0; i < _chains.length; i++) {
288:        for (uint256 i = 0; i < _chains.length; i++) {
307:        for (uint256 i = 0; i < contactsLength; ++i) {
314:        for (uint256 i = 0; i < chainsLength; ++i) {
321:            for (uint256 j = 0; j < accts.length; ++j) {
365:        for (uint256 i = 0; i < length; ++i) {
378:        for (uint256 i = 0; i < length; i++) {
398:        for (uint256 i = 0; i < chainAccounts.length; i++) {

SafeHarborRegistry.sol
34:        uint256 migratedCount = 0;
36:        for (uint256 i = 0; i < length; i++) {

ChainValidator.sol
39:        for (uint256 i = 0; i < length; i++) {
64:        for (uint256 i = 0; i < length; i++) {
80:        for (uint256 i = 0; i < length; i++) {
```

**SafeHarbor:**
Fixed in commit [ed67312](https://github.com/PatrickAlphaC/safe-harbor/commit/ed67312d7679596fe554503406283bd9194430bb).

**Cyfrin:** Verified.
