---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-bridgex-v2-0-2-9
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-bridgex-v2-0
title: Sanity check correct `chainId` matches current chain in `PublicBridge, PrivateChainBridge::_releaseTokens`
vuln_class: []
---

# Sanity check correct `chainId` matches current chain in `PublicBridge, PrivateChainBridge::_releaseTokens`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-bridgex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md)_

---

**Description:** `PublicBridge::_releaseTokens` fetches the `chainId` for the input `destinationChain` but never verifies that the `chainId` matches the current chain. Consider adding in this validation to prevent a scenario where the releasers sign for the incorrect `destinationChain`:
```diff

  function _releaseTokens(
      address to,
      uint256 amount,
      DestinationChain destinationChain
  ) internal returns (bool) {
+     uint256 chainId = getChainId(destinationChain);
+     require(chainId == block.chainid, "Invalid destination chain for this bridge");

      uint256 vaultBalance = token.balanceOf(address(vault));
      // ... rest unchanged but use `chainId` instead of calling `getChainId`
```

A similar fix should be implemented in `PrivateChainBridge::_releaseTokens` to enforce that `destinationChain == DestinationChain.Private`.

**BridgeX:**
Fixed in commit [f9686e8](https://github.com/NerdUnited-NodeGovernance/audit-2026-03-bridgex/commit/f9686e850067e5deaae6ca97077a666539086821).

**Cyfrin:** Verified.

\clearpage
