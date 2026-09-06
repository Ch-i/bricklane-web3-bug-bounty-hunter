---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-23-cyfrin-ens-registrar-manager-v2-0-0-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-03-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-23-cyfrin-ens-registrar-manager-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-23-cyfrin-ens-registrar-manager-v2-0
title: Permissionless `withdrawAll` allows frontrunning a pending destination change
vuln_class: []
---

# Permissionless `withdrawAll` allows frontrunning a pending destination change

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-23-cyfrin-ens-registrar-manager-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-23-cyfrin-ens-registrar-manager-v2.0.md)_

---

**Description:** `withdrawAll` is permissionless, meaning anyone can call it at any time to pull ETH from all registrars and forward the full contract balance to `destination`. If the owner needs to change `destination` via `setDestination` (e.g. because the Endowment Safe is compromised or its signers have lost access), a frontrunner can observe the pending `setDestination` transaction and call `withdrawAll` first, sending all accumulated ETH to the old `destination`.

Since the owner is the ENS DAO Timelock, the `setDestination` call goes through a governance delay. During that entire window, funds keep accumulating in the registrars and anyone can repeatedly call `withdrawAll` to drain them to the stale address.

[RegistrarManager.sol#L176-L184](https://github.com/blockful/dao-proposals/blob/6eaea8c/RegistrarManager/src/ens/proposals/ep-registrar-manager-endowment/contracts/RegistrarManager.sol#L176-L184)

```solidity
function withdrawAll() external {
    address registrar = _next[_HEAD];
    while (registrar != _HEAD) {
        bool success = _withdrawRegistrar(registrar);
        emit RegistrarWithdrawn(registrar, success);
        registrar = _next[registrar];
    }
    _forwardBalance();
}
```

**Impact:** If the Endowment Safe (`0x4F2083f5fBede34C2714aFfb3105539775f7FE64`) is compromised or its signers lose access, all ETH held across managed registrars can be forwarded there before the DAO can update `destination` through governance. The loss is the full balance at the time of the frontrun, and repeated calls can keep draining any newly accumulated ETH until the governance proposal finalizes.

**Recommended Mitigation:** Add an owner-only pause mechanism that stops `withdrawAll` from executing while a `destination` change is pending. Alternatively, bundle the `setDestination` call atomically with a `withdrawAll` in the same governance proposal so the old destination is never used after the decision to change it.

```solidity
bool public paused;

function setPaused(bool _paused) external onlyOwner {
    paused = _paused;
}

function withdrawAll() external {
    require(!paused, "paused");
    // ...existing logic
}
```

**Blockful:**
Acknowledged. The risk is conditional on the Endowment Safe being compromised, and the current destination being DAO-controlled mitigates the concern.
