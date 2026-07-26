---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-16-cyfrin-d2-hype-corewriter-v2-0-0-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-10-16T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-d2-hype-corewriter-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-16-cyfrin-d2-hype-corewriter-v2-0
title: Native HYPE transfers to HyperCore will not work
vuln_class: []
---

# Native HYPE transfers to HyperCore will not work

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-16-cyfrin-d2-hype-corewriter-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-d2-hype-corewriter-v2.0.md)_

---

**Description:** `Hype_Module::hyper_depositSpot` always calls `IERC20(token).transfer(assetAddress(uint64(asset)), _wei)`, including when `asset == 150` (native HYPE). Per HyperCore [docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/hyperevm/hypercore-less-than-greater-than-hyperevm-transfers#transferring-hype), HYPE (id `150`) must be transferred as native value to the special system address `0x2222…2222`, not via ERC-20. In addition, when transferring native HYPE the `token` parameter should be a placeholder (the zero address) to avoid ambiguity and accidental ERC-20 paths.

**Impact:** Native HYPE transfers will likely not work as the token parameter will either be a placeholder or, worst case a wrapped version where the transfer might succeed but the crediting of tokens on HyperCore will fail (as the asset id is wrong) resulting in lost tokens. It can also create ambiguity around the `token` parameter for native deposits can lead to misconfiguration or silent misrouting of funds.

**Recommended mitigation:**

* Make `hyper_depositSpot` `payable` and branch on `asset`:

  * If `asset == 150` (HYPE/native): require `token == address(0)` and `msg.value == _wei`, then send native value to `0x2222…2222`:

    ```diff
      function hyper_depositSpot(
          address token,
          uint32 asset,
          uint64 _wei
    - ) external onlyRole(EXECUTOR_ROLE) nonReentrant {
    + ) external payable onlyRole(EXECUTOR_ROLE) nonReentrant {
    +     if (asset == 150) {
    +         require(token == address(0), "token must be zero for HYPE");
    + 	      require(msg.value == _wei, "msg.value mismatch");
    +         (bool ok, ) = address(0x2222222222222222222222222222222222222222).call{value: _wei}("");
    + 	      require(ok, "native HYPE transfer failed");
    +         return;
    +     }

          IERC20(token).transfer(assetAddress(uint64(asset)), _wei);
      }
    ```
* Optionally overload or split the API (`hyper_depositSpotHype(uint64 _wei)` vs `hyper_depositSpotERC20(address token, uint32 asset, uint256 amount)`) to remove ambiguity.


**D2:** Fixed in commit [`134a2b1`](https://github.com/d2sd2s/d2-contracts/commit/134a2b1c4d40de852b60a3124f8e8ded9a025668) except for the part where we make it payable and check the msg.value as it's meant to transfer funds IN the strategy contract, not funds owned by the sender / operator.

**Cyfrin:** Verified. If `asset == 150` the Hype module now calls `0x22...22` with `value: _wei`.
