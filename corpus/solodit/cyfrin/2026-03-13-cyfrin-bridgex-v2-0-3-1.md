---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-bridgex-v2-0-3-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-bridgex-v2-0
title: In Solidity don't initialize to default values
vuln_class: []
---

# In Solidity don't initialize to default values

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-bridgex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md)_

---

**Description:** In Solidity don't initialize to default values:
```solidity
PublicBridge.sol
73:    bool public paused = false;
348:        for (uint i = 0; i < releasers.length; i++) {
389:        uint256 distributed = 0;
390:        for (uint i = 0; i < releasers.length; i++) {
576:        for (uint i = 0; i < releases.length && eligibleBridgeReleases[recipient] > 0; i++) {
606:        uint256 remainingCount = 0;
607:        for (uint i = 0; i < releases.length; i++) {
617:            for (uint i = 0; i < pendingRecipients.length; i++) {
626:            uint256 index = 0;
628:            for (uint i = 0; i < releases.length; i++) {
636:            for (uint i = 0; i < newReleases.length; i++) {

PrivateChainBridge.sol
74:    bool public paused = false;
332:        for (uint i = 0; i < releasers.length; i++) {
387:        uint256 distributed = 0;
388:        for (uint i = 0; i < releasers.length; i++) {
553:        for (uint i = 0; i < releases.length && eligibleBridgeReleases[recipient] > 0; i++) {
581:        uint256 remainingCount = 0;
582:        for (uint i = 0; i < releases.length; i++) {
592:            for (uint i = 0; i < pendingRecipients.length; i++) {
601:            uint256 index = 0;
603:            for (uint i = 0; i < releases.length; i++) {
611:            for (uint i = 0; i < newReleases.length; i++) {
```

**BridgeX:**
Fixed in commit [bd98983](https://github.com/NerdUnited-NodeGovernance/audit-2026-03-bridgex/commit/bd989836069abbd3958c35a350f07ef4e6ea78b2).

**Cyfrin:** Verified.
