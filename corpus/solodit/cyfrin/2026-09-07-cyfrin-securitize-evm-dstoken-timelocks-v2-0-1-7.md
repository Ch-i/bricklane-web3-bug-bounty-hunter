---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2-0-1-7
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-09-07T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2-0
title: '`DSToken::setMintCap, setOverCapGracePeriod` accept unbounded inputs, so a
  mistaken governance proposal causes an issuance outage lasting at least one timelock
  delay'
vuln_class: []
---

# `DSToken::setMintCap, setOverCapGracePeriod` accept unbounded inputs, so a mistaken governance proposal causes an issuance outage lasting at least one timelock delay

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2.0.md)_

---

**Description:** Neither setter bounds its period argument, Both accept the maximum unsigned value without reverting:
* `setMintCap` requires only that the window be non-zero while a cap is active
* `setOverCapGracePeriod` validates nothing at all

The resulting state is only detected later, by the arithmetic that consumes it. `DSToken::_checkThrottle` computes `windowStart + mintCapWindow`, and `scheduleOverCapIssuance` computes `readyAt + overCapGracePeriod`, both under checked arithmetic. An extreme value therefore stores successfully and then makes every subsequent call revert with an unnamed arithmetic panic that names neither the parameter nor the cause.

**Impact:** The setter succeeding is what makes this matter. After handover these parameters are set by the master timelock, so a wrong value is not a typo an operator can retract - it is a proposal that has already been scheduled, waited out its delay, and executed. Correcting it requires a fresh proposal through the same queue, so the minimum outage is one full master delay, forty eight hours at the deployment default, during which no issuance is possible on the affected path.

**Recommended Mitigation:** Bound both parameters at the point where the value is accepted, so a mistaken proposal reverts on execution rather than committing a state that breaks the contract afterwards:

```solidity
require(_mintCapAmount == 0 || (_mintCapWindow >= MIN_WINDOW && _mintCapWindow <= MAX_WINDOW), "Invalid mint cap window");
require(_overCapGracePeriod <= MAX_GRACE_PERIOD, "Invalid grace period");
```

Reasonable constants such as one hour to one year make every reachable configuration safe and cost one comparison. A proposal that fails during execution is recoverable immediately; one that succeeds and bricks issuance is not.

**Securitize:** Acknowledged.
