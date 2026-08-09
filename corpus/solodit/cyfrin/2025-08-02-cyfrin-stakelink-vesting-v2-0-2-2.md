---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-02-cyfrin-stakelink-vesting-v2-0-2-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-08-02T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-02-cyfrin-stakelink-vesting-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-02-cyfrin-stakelink-vesting-v2-0
title: '`SDLVesting::stakeReleasableTokens` gas optimization by caching variables'
vuln_class: []
---

# `SDLVesting::stakeReleasableTokens` gas optimization by caching variables

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-02-cyfrin-stakelink-vesting-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-02-cyfrin-stakelink-vesting-v2.0.md)_

---

**Description:**
```solidity
    function stakeReleasableTokens() external {
        uint256 amount = releasable();
        if (amount == 0) revert NoTokensReleasable();

        released += amount;
        sdlToken.transferAndCall(
            address(sdlPool),
            amount,
            abi.encode(reSDLTokenIds[lockTime], lockTime * (365 days))
        );

        if (reSDLTokenIds[lockTime] == 0) {
            reSDLTokenIds[lockTime] = sdlPool.lastLockId();
        }

        emit Staked(amount);
    }
```

Currently `lockTime` and `reSDLTokenIds[lockTime]` are read from storage for multiple times. Both variables should be cached to save gas:

```diff
    function stakeReleasableTokens() external {
        uint256 amount = releasable();
        if (amount == 0) revert NoTokensReleasable();

        released += amount;
-       sdlToken.transferAndCall(
-           address(sdlPool),
-           amount,
-           abi.encode(reSDLTokenIds[lockTime], lockTime * (365 days))
-       );
-
-       if (reSDLTokenIds[lockTime] == 0) {
-           reSDLTokenIds[lockTime] = sdlPool.lastLockId();
-       }

+       uint64 cachedLockTime = lockTime;
+       uint256 cachedTokenId = reSDLTokenIds[cachedLockTime];
+
+       sdlToken.transferAndCall(
+          address(sdlPool),
+          amount,
+         abi.encode(cachedTokenId, cachedLockTime * (365 days))
+      );
+
+      if (cachedTokenId == 0) {
+          reSDLTokenIds[cachedLockTime] = sdlPool.lastLockId();
+      }

       emit Staked(amount);
    }
```

**Stake.Link:** Fixed in commit [`128c335`](https://github.com/stakedotlink/contracts/commit/128c33560d8f43057c5d10d822b4904d0762d0fd)

**Cyfrin:** Verified. `tokenId` now cached.
