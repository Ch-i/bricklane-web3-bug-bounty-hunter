---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-bridgex-v2-0-2-5
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-bridgex-v2-0
title: Use explicit `uint256` instead of `uint`
vuln_class: []
---

# Use explicit `uint256` instead of `uint`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-bridgex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md)_

---

**Description:** Use explicit `uint256` instead of `uint`:
```solidity
PublicBridge.sol
332:        for (uint i = 0; i < releasers.length; i++) {
374:        for (uint i = 0; i < releasers.length; i++) {
560:        for (uint i = 0; i < releases.length && eligibleBridgeReleases[recipient] > 0; i++) {
591:        for (uint i = 0; i < releases.length; i++) {
601:            for (uint i = 0; i < pendingRecipients.length; i++) {
612:            for (uint i = 0; i < releases.length; i++) {
620:            for (uint i = 0; i < newReleases.length; i++) {

PrivateChainBridge.sol
320:        for (uint i = 0; i < releasers.length; i++) {
376:        for (uint i = 0; i < releasers.length; i++) {
541:        for (uint i = 0; i < releases.length && eligibleBridgeReleases[recipient] > 0; i++) {
570:        for (uint i = 0; i < releases.length; i++) {
580:            for (uint i = 0; i < pendingRecipients.length; i++) {
591:            for (uint i = 0; i < releases.length; i++) {
599:            for (uint i = 0; i < newReleases.length; i++) {

Token.sol
7:    function transfer(address recipient, uint amount) external returns (bool);
8:    function transferFrom(address sender, address recipient, uint amount) external returns (bool);
9:    function approve(address spender, uint amount) external returns (bool);
12:    event Transfer(address indexed from, address indexed to, uint value);
13:    event Approval(address indexed owner, address indexed spender, uint value);
```

**BridgeX:**
Fixed in commit [97b6c65](https://github.com/NerdUnited-NodeGovernance/audit-2026-03-bridgex/commit/97b6c6589301b2f662d66e25a22a87a3f4627897) for `PublicBridge, PrivateChainBridge`.

**Cyfrin:** Verified.
