---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-14-cyfrin-goldilocks-v1-1-0-4
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-04-14T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md
tags:
- firm:cyfrin
- report:2024-04-14-cyfrin-goldilocks-v1-1
title: In `GovLocks`, it shouldn't use a `deposits` mapping
vuln_class: []
---

# In `GovLocks`, it shouldn't use a `deposits` mapping

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-14-cyfrin-goldilocks-v1.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md)_

---

**Severity:** High

**Description:** In `GovLocks`, it tracks every user's deposit amount using a `deposits` mapping.
As users can transfer `govLocks` freely, they might have fewer `deposits` than their `govLocks` balance and wouldn't be able to withdraw when they want.

```solidity
  function deposit(uint256 amount) external {
    deposits[msg.sender] += amount; //@audit no need
    _moveDelegates(address(0), delegates[msg.sender], amount);
    SafeTransferLib.safeTransferFrom(locks, msg.sender, address(this), amount);
    _mint(msg.sender, amount);
  }

  /// @notice Withdraws Locks to burn Govlocks
  /// @param amount Amount of Locks to withdraw
  function withdraw(uint256 amount) external {
    deposits[msg.sender] -= amount; //@audit no need
    _moveDelegates(delegates[msg.sender], address(0), amount);
    _burn(msg.sender, amount);
    SafeTransferLib.safeTransfer(locks, msg.sender, amount);
  }
```

Here is a possible scenario.
- Alice has deposited 100 `LOCKS` and got 100 `govLOCKS`. Also `deposits[Alice] = 100`.
- Bob bought 50 `govLOCKS` from Alice to get voting power.
- When Bob tries to call `withdraw()`, it will revert because `deposits[Bob] = 0` although he has 50 `govLOCKS`.

**Impact:** Users wouldn't be able to withdraw `LOCKS` with `govLOCKS`.

**Recommended Mitigation:** We don't need to use the `deposits` mapping at all and we can just rely on `govLocks` balances.

**Client:** Fixed in [PR #8](https://github.com/0xgeeb/goldilocks-core/pull/8)

**Cyfrin:** Verified.
