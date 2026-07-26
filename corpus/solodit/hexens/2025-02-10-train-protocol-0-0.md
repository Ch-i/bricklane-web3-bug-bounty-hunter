---
affected_contracts: []
derives_from: []
id: solodit-hexens-2025-02-10-train-protocol-0-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-02-10T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2025-02-10-Train-Protocol.md
tags:
- firm:hexens
- report:2025-02-10-train-protocol
title: '[LYSWP2-7] The LP can steal the user''s funds by initiating a refund before
  the user executes the redeem function'
vuln_class: []
---

# [LYSWP2-7] The LP can steal the user's funds by initiating a refund before the user executes the redeem function

_Section severity (from Solodit section header): High_  
_Audit firm: Hexens_  
_Source report: [2025-02-10-Train-Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2025-02-10-Train-Protocol.md)_

---

**Severity:** High

**Path:** chains/evm/solidity/contracts/HashedTimeLockERC20.sol#L172-L176 

**Description:** The timelock for all user and LP locks is enforced to be at least 15 minutes. However, LPs can exploit this by setting their lock duration to the minimum (15 minutes). This is because users must call `addLock()` after the LPs lock their tokens, ensuring that the user's timelock is always longer than the LP's timelock.

As a result, at the LP’s `timelock` expiration, the LP can call `refund()` on the destination chain to reclaim their tokens and then call redeem() on the source chain to claim the user’s funds. Meanwhile, the user is unable to retrieve their funds since their `timelock` has not yet expired.

Exploit Scenario:
1. Alice (the user) creates a commit object on the source chain, setting Bob (the LP) as `srcReceiver = Bob`.

2. At timestamp T, Bob sees the event on the source chain and locks tokens on the destination chain with a timelock of T + 900 (15 minutes).

3. Alice must call `addLock()` to finalize her commitment, which always happens after Bob’s lock is created. Consequently, Alice's timelock is always longer than Bob’s.

4. At T + 900, Bob calls `refund()` on the destination chain to reclaim his funds. At this point, Alice’s funds are still locked.

5. Bob then calls `redeem()` on the source chain to claim Alice’s funds.

Outcome: Alice loses her tokens, while Bob profits from the exploit.
```
  /// @dev Modifier to ensure the provided timelock is at least 15 minutes in the future.
  modifier _validTimelock(uint48 timelock) {
    if (block.timestamp + 900 > timelock) revert InvalidTimelock();
    _;
  }
```

**Remediation:**  The issue can be partially mitigated by forcing the LP lock their tokens at least 30 minutes (2 * 15 minutes). 

**Status:**  Fixed


- - -
