---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-08-cyfrin-lido-circuit-breaker-v2-0-0-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-04-08T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-08-cyfrin-lido-circuit-breaker-v2.0.md
tags:
- firm:cyfrin
- report:2026-04-08-cyfrin-lido-circuit-breaker-v2-0
title: Single pauser per pausable combined with heartbeat expiry lockout leaves zero
  emergency coverage during liveness gaps
vuln_class: []
---

# Single pauser per pausable combined with heartbeat expiry lockout leaves zero emergency coverage during liveness gaps

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-08-cyfrin-lido-circuit-breaker-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-08-cyfrin-lido-circuit-breaker-v2.0.md)_

---

**Description:** Each pausable contract can only have one configured pauser in `CircuitBreaker`. If that pauser's heartbeat expires, they are completely locked out — both `CircuitBreaker::heartbeat` and `CircuitBreaker::pause` require `isPauserLive` to return true (via `_updateHeartbeat` with `_requireActive = true`):

```solidity
// CircuitBreaker.sol
246:    function heartbeat() external {
247:        require(registry.isRegistered(msg.sender), SenderNotPauser());
248:        _updateHeartbeat(msg.sender, true);  // requires live
249:    }

255:    function pause(address _pausable) external nonReentrant {
256:        require(msg.sender == registry.getPauser(_pausable), SenderNotPauser());
257:        _updateHeartbeat(msg.sender, true);  // requires live

276:    function _updateHeartbeat(address _pauser, bool _requireActive) internal {
277:        if (_requireActive) require(isPauserLive(_pauser), HeartbeatExpired());
```

The only way to restore an expired pauser is the [admin](https://etherscan.io/address/0x3e40D73EB977Dc6a537aF587D48316feE66E9C8c) calling `CircuitBreaker::registerPauser` to re-register them — this calls `_updateHeartbeat(_newPauser, false)` which bypasses the liveness check.

This creates a gap: between heartbeat expiry and admin re-registration, the pausable contract has zero emergency pause coverage through `CircuitBreaker`. If an emergency occurs during this window, the slow governance path is the only option — exactly the scenario `CircuitBreaker` was built to prevent.

The design rationale is sound ("A committee that cannot prove its liveness should not be trusted to respond in an emergency"), but the single-pauser-per-pausable constraint means there is no fallback. Consider whether the `Registry` contract used by `CircuitBreaker` should support multiple pausers for each pausable contract.

**Lido:** Acknowledged as:
* Single pauser keeps accountability clear
* Expiry is the enforcement mechanism; a committee that can't send one heartbeat transaction once per year (for example) shouldn't hold pause authority
* Heartbeat expiry is fully trackable; off-chain monitoring can alert pausers months in advance before expiry
* the tradeoff of having no fallback is accepted

\clearpage
