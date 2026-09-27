---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-02-04-dutch-protocol-1-4
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-02-04T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md
tags:
- firm:codespect
- report:2026-02-04-dutch-protocol
title: '[M-05] The contribute(...) function may be DoS'
vuln_class: []
---

# [M-05] The contribute(...) function may be DoS

_Section severity (from Solodit section header): Medium_  
_Audit firm: CODESPECT_  
_Source report: [2026-02-04-Dutch-Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md)_

---

**Files:** [`AuctionAssist.sol`](https://github.com/dutch-protocol/Protocol-Contracts/tree/cec8b243aa645fdbe80e05e613eca69542b62a2e/src/AuctionAssist.sol#L272)

**Description:**

In `AuctionAssist`, each collection can have a maximum of 100 contributors to prevent excessive loops from causing gas exhaustion.

```solidity
function contribute(address collection_) external payable nonReentrant whenNotPaused{
    //...
    if (!_hasContributed[collection_][msg.sender]) {
        // Check max contributors limit.
        if (_collectionContributors[collection_].length >= MAX_CONTRIBUTORS)
        {
            revert MaxContributorsExceeded();
        }
        //...
    }
}
```

However, a malicious actor can switch accounts and contribute 1 wei 100 times to reach the contributor limit, preventing funds from being raised.

**Impact:** The fund-raising functionality of `AuctionAssist` may be vulnerable to a DoS attack.

**Recommendation:** It is recommended to refactor the code logic and use alternative methods to avoid excessive gas consumption.

**Status:** Fixed

**Client response:** Fixed by commit [8e583e00553d9178e8204bacda50fdfcaffae9f4](https://github.com/dutch-protocol/Protocol-Contracts/commit/8e583e00553d9178e8204bacda50fdfcaffae9f4)

**CODESPECT fix review:** We believe this issue has only been partially fixed. Although setting a minimum contribution amount mitigates dust attacks to some extent, `AuctionAssist` may still become unusable in the long run. The reasons are:

- Each collection allows a maximum of 100 contributors.
- The contributors array has no cleanup mechanism and can only continue to grow. In this situation, even if some contributors' balances are reduced to zero, they still occupy slots in the array. Over time, this may prevent new valid contributors from being added, ultimately blocking the contract's functionality. Additionally, an attacker can still increase the array length by repeatedly calling `contribute` and then immediately `withdrawContribution`.

**CODESPECT fix review recommendations:**

- Add a cleanup mechanism to remove contributors from the array when their balances are zeroed.
- Additionally, provide an admin-controlled queue cleanup mechanism to manually remove malicious contributor records when necessary.

**Client response:** Fixed in [PR-124](https://github.com/dutch-protocol/Protocol-Contracts/pull/124)

**CODESPECT fix review:** The above fix initially establishes a clearing mechanism, and it is also recommended to add an admin clearing mechanism for withdrawing small `_contributions`. Additionally, when processing refunds, if sending ETH fails in admin clear, the funds that were not successfully sent are stored in a mapping to allow later claims, preventing DoS.

**Client response:** Good call, pushed into the same PR [e04b86410fcf5c6d066d4908c67b968071864f08](https://github.com/dutch-protocol/Protocol-Contracts/pull/124/changes/e04b86410fcf5c6d066d4908c67b968071864f08)
