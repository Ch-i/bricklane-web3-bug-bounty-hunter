---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-02-04-dutch-protocol-2-1
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-02-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md
tags:
- firm:codespect
- report:2026-02-04-dutch-protocol
title: '[L-02] Failed vesting stream creation causes permanent loss of contributor
  funds'
vuln_class: []
---

# [L-02] Failed vesting stream creation causes permanent loss of contributor funds

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2026-02-04-Dutch-Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md)_

---

**Files:** [`Presale.sol`](https://github.com/dutch-protocol/Protocol-Contracts/tree/cec8b243aa645fdbe80e05e613eca69542b62a2e/src/Presale.sol)

**Description:**

The `_createVestingStreams(...)` function iterates through all contributors to create Sablier vesting streams for their token allocations. If stream creation fails for any contributor, the function catches the error, emits an event, and continues to the next contributor. However, there is no fallback mechanism to recover the funds of the failed contributor.

```solidity
function _createVestingStreams() internal {
    // ...
    for (uint256 i = 0; i < contributorCount; i++) {
        address contributor = contributors[i];
        uint256 userTokenAllocation = (totalTokens * userContribution) / totalFundedAmount;

        // ...

        try sablierV2.createWithDurationsLL(params, unlockAmounts, durations)
            returns (uint256 streamId) {
            vestingStreamIds[contributor] = streamId;
            streamsCreated++;
            emit TokensClaimed(contributor, userTokenAllocation);
        } catch {
            // @audit Tokens stuck - no recovery mechanism
            emit StreamCreationFailed(contributor, userTokenAllocation);
            continue;

            // ! no fallback method to return the funds to the user
        }
    }
}
```

**Impact:** Contributors who experience failed stream creation permanently lose both their ETH contribution and their token allocation. The tokens remain stuck in the `Presale` contract with no recovery path.

**Recommendation:** Implement a fallback claiming mechanism for failed streams.

**Status:** Fixed

**Client response:** Commit [b6ec15a6aa038829722c1d34079aba58cdcaca6b](https://github.com/dutch-protocol/Protocol-Contracts/commit/b6ec15a6aa038829722c1d34079aba58cdcaca6b)
