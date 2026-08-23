---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-bridgex-v2-0-1-5
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-bridgex-v2-0
title: Pending Releases in `PrivateChainBridge` could be stuck
vuln_class: []
---

# Pending Releases in `PrivateChainBridge` could be stuck

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-bridgex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md)_

---

**Description:** In `PrivateChainBridge`, pending releases are processed via `PrivateChainBridge::_processPendingReleases`, which calls `PrivateChainBridge::_releaseTokens` that reverts when the vault does not have enough native tokens (or the receiver can not receive native tokens because is an smart contract). Because `PrivateChainBridge::_releaseTokens` has no return value and uses a require on vault balance, any insufficient balance condition (or revert inside `vault::release`) will revert the entire transaction, blocking processing of that user’s pending releases and reverting their fee payment, in case that the loop already processed successfull payment it will revert all of them.  This contrasts with `PublicBridge`, where `PublicBridge::_releaseTokens` returns a bool and `PublicBridge::_processPendingReleases` handles failures gracefully by keeping the failing release pending and breaking the loop without reverting the whole transaction.

Private bridge release and processing:
```solidity
    function _processPendingReleases(address recipient) internal {
        PendingRelease[] storage releases = pendingReleasesByRecipient[recipient];

        for (uint i = 0; i < releases.length && eligibleBridgeReleases[recipient] > 0; i++) {
            if (releases[i].exists) {
                eligibleBridgeReleases[recipient]--;

                _releaseTokens(//@audit ok if a single token fail here then the rest of the releases will be stuck
                    payable(releases[i].recipient),
                    releases[i].amount,
                    releases[i].destinationChain
                );
```

```solidity
  function _releaseTokens(
        address payable to,
        uint256 amount,
        DestinationChain destinationChain
    ) internal {
        require(address(vault).balance >= amount, "Insufficient vault balance");

        vault.release(to, amount);

        uint256 chainId = getChainId(destinationChain);

        emit TokensReleased(to, amount, destinationChain, chainId);
    }
```


**Impact:** If `address(vault).balance < amount` for any pending release in `PrivateChainBridge`, `PrivateChainBridge::_releaseTokens` reverts, causing the entire `PrivateChainBridge::_processPendingReleases` call  to revert. The user’s pending releases cannot be processed until the vault is fully funded for the first failing release, effectively blocking all the user’s queued releases behind it.


**Recommended Mitigation:** Align `PrivateChainBridge` behavior with `PublicBridge` non-reverting pattern.

**BridgeX:**
Fixed in commit [e390a56](https://github.com/NerdUnited-NodeGovernance/bridge-x-contracts/commit/e390a56203b64f7a56b0c2e7b91850e2418bb1e2).

**Cyfrin:** Verified.
