---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-bridgex-v2-0-3-5
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-bridgex-v2-0
title: In `PublicBridge, PrivateChainBridge::payReleaseFee` don't interate over `releasers`
  array when `feePerReleaser` is zero
vuln_class: []
---

# In `PublicBridge, PrivateChainBridge::payReleaseFee` don't interate over `releasers` array when `feePerReleaser` is zero

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-bridgex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md)_

---

**Description:** In `PublicBridge, PrivateChainBridge::payReleaseFee` don't interate over `releasers` array when `feePerReleaser` is zero:
```solidity
        // Distribute fees directly to releasers (skip failures to prevent DoS)
        uint256 distributed = 0;

        if(feePerReleaser > 0) {
            for (uint i = 0; i < releasers.length; i++) {
                (bool success, ) = payable(releasers[i]).call{value: feePerReleaser}("");
                if (success) {
                    distributed += feePerReleaser;
                }
            }
        }
```

Since reading from `storage` is expensive, there's no need to iterate over the entire `releasers` array in storage when `feePerReleaser == 0`.

**BridgeX:**
Fixed in commit [cef83f7](https://github.com/NerdUnited-NodeGovernance/audit-2026-03-bridgex/commit/cef83f75c36c6bbe39e6ccc26501d4885a725331).

**Cyfrin:** Verified.
