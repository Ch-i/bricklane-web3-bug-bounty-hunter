---
affected_contracts: []
derives_from: []
id: solodit-hexens-2025-02-10-train-protocol-2-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-02-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2025-02-10-Train-Protocol.md
tags:
- firm:hexens
- report:2025-02-10-train-protocol
title: '[LYSWP2-13] Id should be checked by the LP before redeeming'
vuln_class: []
---

# [LYSWP2-13] Id should be checked by the LP before redeeming

_Section severity (from Solodit section header): Low_  
_Audit firm: Hexens_  
_Source report: [2025-02-10-Train-Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2025-02-10-Train-Protocol.md)_

---

**Severity:** Low

**Path:** chains/evm/solidity/contracts/HashedTimeLockERC20.sol#L253-L272 

**Description:** When a user calls the `addLock()` function, an event containing the HTLC ID, hashlock, and timelock is emitted. The Solver implementation documentation recommends verifying the correctness of the hashlock and timelock.

However, if the Solver does not verify which HTLC ID the hashlock and timelock correspond to and only checks their validity, an attacker could deceive the LP by associating the hashlock with a different HTLC—one that locks a lower amount than originally committed. This exploit would enable the attacker to receive significantly more tokens on the destination chain than they locked on the source chain.
```
function addLock(
    bytes32 Id,
    bytes32 hashlock,
    uint48 timelock
  ) external _exists(Id) _validTimelock(timelock) nonReentrant returns (bytes32) {
    HTLC storage htlc = contracts[Id];
    if (htlc.claimed == 2 || htlc.claimed == 3) revert AlreadyClaimed();
    if (msg.sender == htlc.sender) {
      if (htlc.hashlock == bytes32(bytes1(0x01))) {
        htlc.hashlock = hashlock;
        htlc.timelock = timelock;
      } else {
        revert HashlockAlreadySet(); // Prevent overwriting hashlock.
      }
      emit TokenLockAdded(Id, hashlock, timelock);
      return Id;
    } else {
      revert NoAllowance(); // Ensure only allowed accounts can add a lock.
    }
  }
```

**Remediation:**  Documentation should add the verification of the ID as an important step in the Solver implementation guide.

**Status:** Fixed

- - -
