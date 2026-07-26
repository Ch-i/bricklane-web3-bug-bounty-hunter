---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-23-cyfrin-ens-registrar-manager-v2-0-0-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-03-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-23-cyfrin-ens-registrar-manager-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-23-cyfrin-ens-registrar-manager-v2-0
title: ETH-forwarding call via `execOnRegistrar` can be griefed by front-running with
  `withdrawAll`
vuln_class: []
---

# ETH-forwarding call via `execOnRegistrar` can be griefed by front-running with `withdrawAll`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-23-cyfrin-ens-registrar-manager-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-23-cyfrin-ens-registrar-manager-v2.0.md)_

---

**Description:** `execOnRegistrar` allows the owner to make arbitrary calls to a managed registrar, optionally attaching ETH from the RegistrarManager's own balance via the `value` parameter:

```solidity
// RegistrarManager.sol line 199–213
function execOnRegistrar(
    address registrar,
    uint256 value,       // ← ETH drawn from address(this).balance
    bytes calldata data
)
    external onlyOwner returns (bool success, bytes memory result)
{
    if (!isRegistrar(registrar)) revert RegistrarNotFound(registrar);
    (success, result) = registrar.call{ value: value }(data);  // ← silent failure if balance < value
    emit RegistrarCall(registrar, value, data, success);
}
```

Because `withdrawAll` is **permissionless**, a griefer can front-run the owner's pending `execOnRegistrar` transaction with a `withdrawAll()` call, draining the RegistrarManager's ETH balance to `destination` before the governance transaction lands. When `execOnRegistrar` then executes, `address(this).balance < value` and the low-level call silently fails — returning `success = false` without reverting.

**Attack Scenario:**

1. The DAO passes a governance proposal calling `execOnRegistrar(registrar, 5 ether, data)` to fund or interact with a registrar with ETH
2. The RegistrarManager holds 5 ETH (accumulated from prior registrar withdrawals)
3. A griefer sees the pending governance transaction in the mempool and front-runs with `withdrawAll()`
4. `withdrawAll()` drains the 5 ETH from RegistrarManager to the Endowment Safe
5. `execOnRegistrar` executes — `address(this).balance == 0`, the call to the registrar fails silently with `success = false`
6. The governance action is wasted; a new proposal must be created and wait through the full governance delay


**Impact:** No ETH is stolen — funds are forwarded to the Endowment Safe (the intended long-term destination). However, the Timelock's intended governance action fails silently, and recovery requires creating and waiting through a full new governance proposal cycle. This attack can be repeated indefinitely at near-zero cost to the griefer (only gas).

**Recommended Mitigation:** There are a couple of alternatives to mitigate this issue:

1. When the owner intends to send ETH to a registrar via `execOnRegistrar`, the ETH should be included directly as `msg.value` in the governance transaction rather than relying on the contract's accumulated balance. Add a `payable` modifier to `execOnRegistrar` and use `msg.value` for the call.
2. Similar recommendation as in [*Permissionless `withdrawAll` allows frontrunning a pending destination change*](#permissionless-withdrawall-allows-frontrunning-a-pending-destination-change) . Add a pauser modifier that in case of facing a DoS, the `withdrawAll` function can be paused.
3. Add an access modifier to `withdrawAll` to allow only authorized entities, fully preventing any possibilities of frontrun.

**Blockful:**
Fixed in commit [e2f7584](https://github.com/blockful/dao-proposals/commit/e2f7584).

**Cyfrin:** Verified. `execOnRegistrar ` function no longer forwards ETH — calls registrar with zero value.

\clearpage
