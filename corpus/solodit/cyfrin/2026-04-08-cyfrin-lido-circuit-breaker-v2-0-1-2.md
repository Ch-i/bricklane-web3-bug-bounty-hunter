---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-08-cyfrin-lido-circuit-breaker-v2-0-1-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-04-08T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-08-cyfrin-lido-circuit-breaker-v2.0.md
tags:
- firm:cyfrin
- report:2026-04-08-cyfrin-lido-circuit-breaker-v2-0
title: Redundant storage read of `registry.pauser[_pausable]` in `CircuitBreaker::pause`
vuln_class: []
---

# Redundant storage read of `registry.pauser[_pausable]` in `CircuitBreaker::pause`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-08-cyfrin-lido-circuit-breaker-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-08-cyfrin-lido-circuit-breaker-v2.0.md)_

---

**Description:** In `CircuitBreaker::pause`, the storage slot `registry.pauser[_pausable]` is read twice via separate library calls:

```solidity
CircuitBreaker.sol
255:    function pause(address _pausable) external nonReentrant {
256:        require(msg.sender == registry.getPauser(_pausable), SenderNotPauser());  // SLOAD 1
257:        _updateHeartbeat(msg.sender, true);
258:
259:        uint256 duration = pauseDuration;
260:        IPausable target = IPausable(_pausable);
261:
262:        registry.setPauser(_pausable, address(0));  // SLOAD 2 (re-reads pauser[_pausable] at Registry.sol:85)
```

`Registry::getPauser` reads `_self.pauser[_pausable]` (Registry.sol:44) for the authorization check. Then `Registry::setPauser` reads the same slot again (Registry.sol:85: `address previousPauser = _self.pauser[_pausable]`) to determine the previous pauser for count management. The value has not changed between reads, so the second SLOAD (100 gas warm) is redundant.

**Recommended Mitigation:** `Registry::setPauser` already reads `previousPauser` — return it via a named return value and use it in `CircuitBreaker::pause` to combine the authorization check with the unregistration:

```diff
 // Registry.sol
-function setPauser(Storage storage _self, address _pausable, address _newPauser) internal {
+function setPauser(Storage storage _self, address _pausable, address _newPauser) internal returns (address previousPauser) {
     require(_pausable != address(0), PausableZero());

-    address previousPauser = _self.pauser[_pausable];
+    previousPauser = _self.pauser[_pausable];

     // ... existing logic unchanged ...
 }
```

```diff
 // CircuitBreaker.sol
 function pause(address _pausable) external nonReentrant {
-    require(msg.sender == registry.getPauser(_pausable), SenderNotPauser());
+    require(msg.sender == registry.setPauser(_pausable, address(0)), SenderNotPauser());
     _updateHeartbeat(msg.sender, true);

     uint256 duration = pauseDuration;
     IPausable target = IPausable(_pausable);

-    registry.setPauser(_pausable, address(0));
     target.pauseFor(duration);
     require(target.isPaused(), PauseFailed());

     emit PauseTriggered(_pausable, msg.sender, duration);
 }
```

**Lido:** Acknowledged; 100 gas saved is negligible compared to the decreased readability for a function call that we hope will never be called. The proposed fix:
* hides state mutation inside an auth check
* returns the previous pauser from `setPauser`, which breaks the standard convention where a setter usually returns the new value (or a success boolean)

\clearpage
