---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-bridgex-v2-0-1-2
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
title: '`PublicBridge, PrivateChainBridge::removeReleaser` can reduce releasers below
  `requiredSignatures`, making all release unprocessable'
vuln_class: []
---

# `PublicBridge, PrivateChainBridge::removeReleaser` can reduce releasers below `requiredSignatures`, making all release unprocessable

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-bridgex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md)_

---

**Description:** `PublicBridge, PrivateChainBridge::removeReleaser` does not validate that `releasers.length` remains at or above `requiredSignatures` after removal:

```solidity
function removeReleaser(address _releaser) external onlyOwner {
    require(isReleaser[_releaser], "Not a releaser");
    isReleaser[_releaser] = false;
    for (uint i = 0; i < releasers.length; i++) {
        if (releasers[i] == _releaser) {
            releasers[i] = releasers[releasers.length - 1];
            releasers.pop();
            break;
        }
    }
    // missing: require(releasers.length >= requiredSignatures)
}
```

While `setRequiredSignatures` validates `_requiredSignatures <= releasers.length`, the reverse check is absent from `removeReleaser`. If the owner removes releasers to bring the count below `requiredSignatures`, the `signatureCount[txHash] >= requiredSignatures` condition in `signRelease` can never be met, making all in-progress and future releases unprocessable.

**Impact:**
- All releases become stuck until the owner either adds releasers back or calls `setRequiredSignatures` with a lower value
- In-progress releases that already have some signatures collected cannot reach the threshold
- Recoverable by the owner, but creates a window where the bridge is non-functional

**Recommended Mitigation:** Add a bounds check to `removeReleaser` in both bridges:

```solidity
function removeReleaser(address _releaser) external onlyOwner {
    require(isReleaser[_releaser], "Not a releaser");
    uint256 releasersLength = releasers.length;
    require(releasersLength > requiredSignatures, "Would break signature threshold");
    // ... existing removal logic ...
}
```

**BridgeX:**
Acknowledged; the owner role is trusted and would typically pause the bridge during relayer rotation. Adding a hard block on removal could hinder emergency response if a relayer is compromised. The owner can adjust `requiredSignatures` as needed.
