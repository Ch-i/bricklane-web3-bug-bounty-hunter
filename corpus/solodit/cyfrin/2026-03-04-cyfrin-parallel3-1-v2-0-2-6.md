---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-04-cyfrin-parallel3-1-v2-0-2-6
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-03-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-04-cyfrin-parallel3-1-v2-0
title: '`IBridgeableTokenP::swapLzTokenToPrincipalToken` interface declares a `uint256`
  return value but `BridgeableTokenP::swapLzTokenToPrincipalToken` returns nothing,
  breaking external integrations'
vuln_class: []
---

# `IBridgeableTokenP::swapLzTokenToPrincipalToken` interface declares a `uint256` return value but `BridgeableTokenP::swapLzTokenToPrincipalToken` returns nothing, breaking external integrations

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-04-cyfrin-parallel3.1-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md)_

---

**Description:** The `IBridgeableTokenP` interface declares `swapLzTokenToPrincipalToken` as returning `uint256`:

```solidity
function swapLzTokenToPrincipalToken(address _to, uint256 _amount) external returns(uint256);
```

However, the actual implementation in `BridgeableTokenP::swapLzTokenToPrincipalToken` has no return value:

```solidity
function swapLzTokenToPrincipalToken(address _to, uint256 _amount) external nonReentrant whenNotPaused {
```

Any external contract calling `swapLzTokenToPrincipalToken` through the `IBridgeableTokenP` interface will have its ABI decoder attempt to decode a `uint256` from the return data. Since the implementation returns nothing, the decoder will revert.

**Impact:** External contracts and protocols integrating with `BridgeableTokenP` through the `IBridgeableTokenP` interface will have their calls revert. Direct calls (not through the interface) are unaffected.

**Proof of Concept:**
1. An external contract holds a reference: `IBridgeableTokenP bridge = IBridgeableTokenP(bridgeAddress);`
2. It calls `uint256 minted = bridge.swapLzTokenToPrincipalToken(user, amount);`
3. The function executes successfully internally, but returns no data
4. The ABI decoder on the caller side expects 32 bytes of return data, finds 0 bytes, and reverts

**Recommended Mitigation:** Either add a return value to the implementation to match the interface:

```solidity
function swapLzTokenToPrincipalToken(address _to, uint256 _amount) external nonReentrant whenNotPaused returns (uint256) {
    // ... existing logic ...
    return principalTokenAmountCredited;
}
```

Or remove the return type from the interface:

```solidity
function swapLzTokenToPrincipalToken(address _to, uint256 _amount) external;
```

**Parallel:** Fixed in commit [68faa40](https://github.com/parallel-protocol/parrallel-tokens/commit/68faa401d4d837bd97ff38e38855bf5db220b77d).

**Cyfrin:** Verified. `BridgeableTokenP::swapLzTokenToPrincipalToken` now returns the amount of `principalToken` actually minted.
