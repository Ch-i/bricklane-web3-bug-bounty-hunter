---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-bridgex-v2-0-1-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-bridgex-v2-0
title: Constructors don't validate `releaseFee > 0`, causing `payReleaseFee` to panic
  with division by zero
vuln_class: []
---

# Constructors don't validate `releaseFee > 0`, causing `payReleaseFee` to panic with division by zero

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-bridgex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md)_

---

**Description:** Both bridge constructors accept `_releaseFee` without validating it is greater than zero:

```solidity
// PublicBridge.sol:302-312
constructor(address _token, uint256 _releaseFee, uint256 _bridgeFee, address _bridgeFeeReceiver) {
    token = IERC20(_token);
    owner = msg.sender;
    releaseFee = _releaseFee; // no validation — allows 0
    // ...
}

// PrivateChainBridge.sol:282-296
constructor(uint256 _releaseFee, uint256 _bridgeFee, address _bridgeFeeReceiver) {
    owner = msg.sender;
    releaseFee = _releaseFee; // no validation — allows 0
    // ...
}
```

While `setReleaseFee` enforces `require(_newFee > 0, "Fee must be positive")`, the constructor has no equivalent check. If deployed with `releaseFee = 0`, the `payReleaseFee` function panics with a division by zero on its first line of computation:

```solidity
// Both bridges: payReleaseFee()
uint256 eligibleReleases = msg.value / releaseFee; // Panic(0x12) when releaseFee == 0
```

**Impact:**
- `payReleaseFee` always panics with an opaque `Panic(0x12)` error instead of a meaningful revert message
- All releases go to pending state since no user can pay the release fee
- Only `forceProcessPendingRelease` (owner-only) can process releases
- Recoverable via `setReleaseFee`, but creates a confusing failure mode at deployment

**Recommended Mitigation:** Add validation in both constructors:

```solidity
require(_releaseFee > 0, "Fee must be positive");
```

**BridgeX:**
Fixed in commit [69b0e8e](https://github.com/NerdUnited-NodeGovernance/bridge-x-contracts/commit/69b0e8e2e0421df80c7a3501090f1380cfef4b94).

**Cyfrin:** Verified.
