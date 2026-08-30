---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-08-cyfrin-lido-circuit-breaker-v2-0-1-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-04-08T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-08-cyfrin-lido-circuit-breaker-v2.0.md
tags:
- firm:cyfrin
- report:2026-04-08-cyfrin-lido-circuit-breaker-v2-0
title: Emit before state change to eliminate temporary variable
vuln_class: []
---

# Emit before state change to eliminate temporary variable

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-08-cyfrin-lido-circuit-breaker-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-08-cyfrin-lido-circuit-breaker-v2.0.md)_

---

**Description:** `CircuitBreaker::_setPauseDuration` and `CircuitBreaker::_setHeartbeatInterval` each declare a `previous*` local variable solely to capture the old storage value for the event. Emitting the event before the state change lets the event read the current storage value directly, eliminating the temporary:

```solidity
// CircuitBreaker.sol lines 289-292
uint256 previousPauseDuration = pauseDuration;
pauseDuration = _newPauseDuration;
emit PauseDurationUpdated(previousPauseDuration, _newPauseDuration);

// CircuitBreaker.sol lines 300-303
uint256 previousHeartbeatInterval = heartbeatInterval;
heartbeatInterval = _newHeartbeatInterval;
emit HeartbeatIntervalUpdated(previousHeartbeatInterval, _newHeartbeatInterval);
```

**Recommended Mitigation:**
```diff
 function _setPauseDuration(uint256 _newPauseDuration) internal {
     require(_newPauseDuration >= MIN_PAUSE_DURATION, PauseDurationBelowMin());
     require(_newPauseDuration <= MAX_PAUSE_DURATION, PauseDurationAboveMax());
-    uint256 previousPauseDuration = pauseDuration;
+    emit PauseDurationUpdated(pauseDuration, _newPauseDuration);
     pauseDuration = _newPauseDuration;
-    emit PauseDurationUpdated(previousPauseDuration, _newPauseDuration);
 }
```

Same pattern for `CircuitBreaker::_setHeartbeatInterval`.

**Lido:** Fixed in commit [11aea85](https://github.com/lidofinance/circuit-breaker/commit/11aea853b83408c4f7902ee2289e77034aa87638).

**Cyfrin:** Verified.
