---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-bridgex-v2-0-3-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-bridgex-v2-0
title: Better storage packing
vuln_class: []
---

# Better storage packing

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-bridgex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md)_

---

**Description:** In Solidity:
* reading and writing from `storage` is expensive
* the order of storage declaration is important as it results in more or less `storage` slots being used to store the same data

Achieve better storage packing by:
* struct `PendingRelease` - declare `destinationChain, exists` after `recipient`
```solidity
PublicBridge.sol
112:    struct PendingRelease {

PrivateChainBridge.sol
103:    struct PendingRelease {
```

**BridgeX:**
Fixed in commit [937ba7c](https://github.com/NerdUnited-NodeGovernance/bridge-x-contracts/commit/937ba7cfe338d80b004dc7dbe9bc811aaab31db4).

**Cyfrin:** Verified.
