---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-bridgex-v2-0-0-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-bridgex-v2-0
title: '`PrivateChainBridge, PublicBridge::lockTokens` allows locking tokens to unconfigured
  destination chains, permanently losing user funds'
vuln_class: []
---

# `PrivateChainBridge, PublicBridge::lockTokens` allows locking tokens to unconfigured destination chains, permanently losing user funds

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-bridgex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md)_

---

**Description:** `PrivateChainBridge::lockTokens` only validates that the destination chain is not `Private`:

```solidity
// PrivateChainBridge.sol:425-426
require(msg.value > 0, "Amount required");
require(destinationChain != DestinationChain.Private, "Cannot bridge to self");
```

The `DestinationChain` enum includes `Reserved4` through `Reserved8` (values 4-8) intended for future chain expansion via `setChainId`. However, a user can call `lockTokens` with any of these Reserved values before the owner configures them. The tokens are locked in the vault, the `TokensLocked` event emits with `chainId = 0` (unconfigured default), and relayers have no corresponding destination bridge to process the release.

```solidity
// PrivateChainBridge.sol:443-461
uint256 chainId = getChainId(destinationChain); // returns 0 for unconfigured chains

emit TokensLocked(
    msg.sender,
    bridgeAmount,
    uniqueHash,
    destinationChain,
    chainId  // 0 — relayers cannot route this
);
```

The locked tokens cannot be recovered — the `TokenVault` has no sweep function and only releases tokens via the bridge's `_releaseTokens` path, which requires relayer signatures from the non-existent destination chain.

**Impact:** Native tokens locked to unconfigured destination chains are irrecoverable; users permanently lose their funds.

**Recommended Mitigation:** Validate that the destination chain has a configured chain ID:

```solidity
function lockTokens(DestinationChain destinationChain) external payable nonReentrant whenNotPaused {
    require(msg.value > 0, "Amount required");
    require(destinationChain != DestinationChain.Private, "Cannot bridge to self");
    uint256 destChainId = getChainId(destinationChain);
    require(destChainId != 0, "Destination chain not configured");
    // ... use destChainId instead of calling getChainId again
}
```

The same fix is required for `PublicBridge::lockTokens`, or alternatively just emit 0 for the chainId if 0 is valid value for the private chain.

**BridgeX:**
Fixed in commits [ab40545](https://github.com/NerdUnited-NodeGovernance/bridge-x-contracts/commit/ab405453d0cbd92b0ea4bbb6817c7c46659fac58), [3320c2b](https://github.com/NerdUnited-NodeGovernance/bridge-x-contracts/commit/3320c2b6d4fd4abba83e40b81a66c6687285c034), [32882e0](https://github.com/NerdUnited-NodeGovernance/bridge-x-contracts/commit/32882e07d78a39d435db99c46950ca286687dca1).

**Cyfrin:** Verified.

\clearpage
