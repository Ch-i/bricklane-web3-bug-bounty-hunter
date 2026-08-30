---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-27-cyfrin-linea-mixed-upgrade-v2-0-1-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-03-27T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-27-cyfrin-linea-mixed-upgrade-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-27-cyfrin-linea-mixed-upgrade-v2-0
title: '`SECURITY_COUNCIL_ROLE` unpausing a type leads to automatically marking as
  expired any other pause types, whether they were enacted by the `SECURITY_COUNCIL_ROLE`
  or not'
vuln_class: []
---

# `SECURITY_COUNCIL_ROLE` unpausing a type leads to automatically marking as expired any other pause types, whether they were enacted by the `SECURITY_COUNCIL_ROLE` or not

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-27-cyfrin-linea-mixed-upgrade-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-27-cyfrin-linea-mixed-upgrade-v2.0.md)_

---

**Description:** `PauseManager` enables the handling of the pausing/unpausing of different `PauseTypes`, targeting specific system functionalities (as well as a `GENERAL` pause). There are two main types of pausers:
1. Pausers with the`SECURITY_COUNCIL_ROLE`
2. Pausers without the `SECURITY_COUNCIL_ROLE`

The main difference between the two is that pausers with `SECURITY_COUNCIL_ROLE` can pause without cooldown or expiry restrictions, and when they unpause, the `pauseExpiryTimestamp` is reset to enable non-`SECURITY_COUNCIL_ROLE` pausing.

There is an edge case that allows for immediately unpause of any active pause after the `SECURITY_COUNCIL_ROLE` unpauses one type. Whether the `SECURITY_COUNCIL_ROLE` unpauses a pause enacted by themselves or by a non-`SECURITY_COUNCIL_ROLE`, the result is the same; any other active pause can be immediately unpaused.

**Impact:** When the `SECURITY_COUNCIL_ROLE` unpauses a type, all the other active pause types will be immediately marked as expired, regardless of whether they were enacted by the `SECURITY_COUNCIL_ROLE` or a `non-SECURITY_COUNCIL_ROLE` account.

**Proof of Concept:** Add the next PoC to `PauseManager.ts`:
```js
    it.only("Non-SECURITY_COUNCIL_ROLE pause L1_L2_PAUSE_TYPE -> SECURITY_COUNCIL_ROLE pause GENERAL_PAUSE_TYPE -> SECURITY_COUNCIL_ROLE unpause L1_L2_PAUSE_TYPE => GENERAL_PAUSE can be unpaused even though it had not been actually unpaused", async () => {
      await pauseByType(L1_L2_PAUSE_TYPE);
      await pauseByType(GENERAL_PAUSE_TYPE, securityCouncil);
      await unPauseByType(L1_L2_PAUSE_TYPE, securityCouncil);
      //@audit-info => GENERAL_PAUSE can be immediately unpaused even though it had not been actually unpaused
      await unPauseByExpiredType(GENERAL_PAUSE_TYPE, nonManager);
      expect(await pauseManager.isPaused(GENERAL_PAUSE_TYPE)).to.be.false;
      expect(await pauseManager.isPaused(L1_L2_PAUSE_TYPE)).to.be.false;
    });
```

**Recommended Mitigation:** Consider not resetting the `pauseExpiryTimestamp` below the `block.timestamp`, potentially add 1 hour cooldown period from the current `block.timestamp`, this will prevent immediately marking other pauses as expired.

Alternatively, consider adding a bool flag to `unpauseByType` flag that can allow the `SECURITY_COUNCIL_ROLE` to select dynamically whether they want to reset the `pauseExpiryTimestamp` or not.
- A more elaborate alternative would be to track the active pauses and reset the `pauseExpiryTimestamp` only when the last active pause is unpaused by the `SECURITY_COUNCIL_ROLE`.

**Linea:** Fixed in [PR 2335](https://github.com/Consensys/linea-monorepo/pull/2335/changes).

**Cyfrin:** Verified. Pause expirations are now tracked per pause type. Non-SecurityCouncil can't pause a pause type already paused by the SecurityCouncil, but the SecurityCouncil can pause a pause type already paused by a non-SecurityCouncil. Pauses enacted by the SecurityCouncil can only be unpaused by them. Unpausing a type only resets the expiry timestamp for that specific type.

\clearpage
