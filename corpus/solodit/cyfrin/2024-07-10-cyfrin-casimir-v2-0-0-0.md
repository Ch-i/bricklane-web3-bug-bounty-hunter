---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-10-cyfrin-casimir-v2-0-0-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-07-10T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md
tags:
- firm:cyfrin
- report:2024-07-10-cyfrin-casimir-v2-0
title: Attacker can cause a DOS during unstaking by intentionally reverting the transaction
  when receiving ETH
vuln_class: []
---

# Attacker can cause a DOS during unstaking by intentionally reverting the transaction when receiving ETH

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-10-cyfrin-casimir-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md)_

---

**Description:** The function `fulfillUnstake()` is used internally to fulfill unstake requests for users. It performs a low-level call to the `userAddress` to transfer ETH and reverses the transaction if the transfer fails. Moreover, the contract processes all unstake requests in a First-In-First-Out (FIFO) queue, meaning it must process earlier requests before handling later ones.

An attacker could exploit this by intentionally triggering a revert on the `receive()` function. This action would cause `fulfillUnstake()` to revert and block the entire unstake queue.
```solidity
function fulfillUnstake(address userAddress, uint256 amount) private {
    (bool success,) = userAddress.call{value: amount}(""); // @audit DOS by reverting on `receive()`
    if (!success) {
        revert TransferFailed();
    }
    emit UnstakeFulfilled(userAddress, amount);
}
```

**Impact:** This can result in a Denial of Service for all unstake requests, thereby locking users’ funds.

**Recommended Mitigation:** Consider using the Pull-over-Push pattern.
Reference: https://fravoll.github.io/solidity-patterns/pull_over_push.html

**Casimir:**
Fixed in [cdbe7b1](https://github.com/casimirlabs/casimir-contracts/commit/cdbe7b1ed9e61a58d7971087e9b6e582eb36a55b)

**Cyfrin:** Verified.
