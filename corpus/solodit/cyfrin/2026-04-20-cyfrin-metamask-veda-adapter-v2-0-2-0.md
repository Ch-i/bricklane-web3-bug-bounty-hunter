---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-20-cyfrin-metamask-veda-adapter-v2-0-2-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2026-04-20T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-20-cyfrin-metamask-veda-adapter-v2.0.md
tags:
- firm:cyfrin
- report:2026-04-20-cyfrin-metamask-veda-adapter-v2-0
title: Use `calldata` instead of `memory` for external function array parameters
vuln_class: []
---

# Use `calldata` instead of `memory` for external function array parameters

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-20-cyfrin-metamask-veda-adapter-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-20-cyfrin-metamask-veda-adapter-v2.0.md)_

---

**Description:** Four external functions accept complex array parameters as `memory` when they are only read, not modified. Using `calldata` avoids an expensive copy from calldata to memory on every call. The two internal helper functions they delegate to can also be changed to `calldata` since they only read the delegations array:

```solidity
// src/helpers/VedaAdapter.sol
201:    function depositByDelegation(Delegation[] memory _delegations, ...) external {
213:    function depositByDelegationBatch(DepositParams[] memory _depositStreams) external {
246:    function withdrawByDelegation(Delegation[] memory _delegations, ...) external {
258:    function withdrawByDelegationBatch(WithdrawParams[] memory _withdrawStreams) external {
331:    function _executeDepositByDelegation(Delegation[] memory _delegations, ...) internal {
369:        Delegation[] memory _delegations,
```

**Recommended Mitigation:** Change `memory` to `calldata` on all six function signatures:

```diff
- function depositByDelegation(Delegation[] memory _delegations, uint256 _minimumMint) external {
+ function depositByDelegation(Delegation[] calldata _delegations, uint256 _minimumMint) external {
```

Apply the same change to all other affected signatures. Update the loop body in batch functions to use `calldata` references accordingly.

**MetaMask:** Fixed in commit [`1f1182e`](https://github.com/MetaMask/delegation-framework/pull/166/changes/1f1182eb9eea88ac5b88d19a753350d9f8bdafb2)

**Cyfrin:** Verified.
