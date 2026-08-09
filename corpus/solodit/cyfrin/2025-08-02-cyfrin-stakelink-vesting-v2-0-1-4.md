---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-02-cyfrin-stakelink-vesting-v2-0-1-4
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-08-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-02-cyfrin-stakelink-vesting-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-02-cyfrin-stakelink-vesting-v2-0
title: '`SDLVesting::withdrawRESDLPositions` enhancements'
vuln_class: []
---

# `SDLVesting::withdrawRESDLPositions` enhancements

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-02-cyfrin-stakelink-vesting-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-02-cyfrin-stakelink-vesting-v2.0.md)_

---

**Description:** The `SDLVesting::withdrawRESDLPositions()` function violates the Checks-Effects-Interactions (CEI) pattern by performing external calls before updating state. The function also lacks input validation for lock times and may attempt to transfer non-existent token IDs, causing transaction reverts and poor user experience.

While not exploitable due to SDLPool's ownership checks, the function updates state after external calls, creating a potential reentrancy vector as well as bad user experience in case of incorrect input.

Consider adding validation for `_lockTimes` and move the state changes before the external call:

```diff
    function withdrawRESDLPositions(uint256[] calldata _lockTimes) external onlyBeneficiary {
        for (uint256 i = 0; i < _lockTimes.length; ++i) {

-            sdlPool.safeTransferFrom(address(this), beneficiary, reSDLTokenIds[_lockTimes[i]]);
-            delete reSDLTokenIds[_lockTimes[i]];

+            if (_lockTimes[i] > MAX_LOCK_TIME) revert InvalidLockTime();
+            uint256 tokenId = reSDLTokenIds[_lockTimes[i]]; // Cache to facilitate the deletion before transfer
+            if (tokenId == 0) continue; // Skip if no reSDL position exists so we don't break execution but also don't attempt to transfer 0.
+            delete reSDLTokenIds[_lockTimes[i]];
+            sdlPool.safeTransferFrom(address(this), beneficiary, tokenId);
        }
    }
```

**Stake.Link:** Fixed in commit [`e458512`](https://github.com/stakedotlink/contracts/commit/e4585124c05137848196d4ca759c3e9d28b963e1)

**Cyfrin:** Verified. `_lockTime[i]` now verified to not be larger than `MAX_LOCK_TIME` and delete is done before call to `safeTransfer`.
