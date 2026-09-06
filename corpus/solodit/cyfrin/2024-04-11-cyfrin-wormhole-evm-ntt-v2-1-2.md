---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-11-cyfrin-wormhole-evm-ntt-v2-1-2
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-04-11T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-11-cyfrin-wormhole-evm-ntt-v2.md
tags:
- firm:cyfrin
- report:2024-04-11-cyfrin-wormhole-evm-ntt-v2
title: NTT Manager cannot be unpaused once paused
vuln_class: []
---

# NTT Manager cannot be unpaused once paused

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-11-cyfrin-wormhole-evm-ntt-v2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-11-cyfrin-wormhole-evm-ntt-v2.md)_

---

**Description:** `NttManagerState::pause` exposes pause functionality to be triggered by permissioned actors but has no corresponding unpause functionality. As such, once the NTT Manager is paused, it will not be possible to unpause without a contract upgrade.
```solidity
function pause() public onlyOwnerOrPauser {
    _pause();
}
```

**Impact:** The inability to unpause the NTT Manager could result in significant disruption, requiring either a contract upgrade or complete redeployment to resolve this issue.

**Recommended Mitigation:**
```diff
+ function unpause() public onlyOwnerOrPauser {
+     _unpause();
+ }
```

**Wormhole Foundation:** Fixed in [PR \#273](https://github.com/wormhole-foundation/example-native-token-transfers/pull/273).

**Cyfrin:** Verified. A corresponding unpause function has been added.
