---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-bridgex-v2-0-2-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-bridgex-v2-0
title: Use named mapping parameters to explicitly denote the purpose of keys and values
vuln_class: []
---

# Use named mapping parameters to explicitly denote the purpose of keys and values

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-bridgex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md)_

---

**Description:** Use named mapping parameters to explicitly denote the purpose of keys and values:
```solidity
PublicBridge.sol
79:    mapping(address => bool) public isReleaser;
100:    mapping(DestinationChain => uint256) public chainIds;
103:    mapping(bytes32 => bool) public processedHashes;
106:    mapping(address => uint256) public eligibleBridgeReleases;
109:    mapping(bytes32 => mapping(address => bool)) public signatures;
112:    mapping(bytes32 => uint256) public signatureCount;
129:    mapping(address => PendingRelease[]) public pendingReleasesByRecipient;
135:    mapping(address => bool) public hasPendingReleases;

PrivateChainBridge.sol
62:    mapping(DestinationChain => uint256) public chainIds;
65:    mapping(address => bool) public isReleaser;
94:    mapping(bytes32 => bool) public processedHashes;
97:    mapping(address => uint256) public eligibleBridgeReleases;
100:    mapping(bytes32 => mapping(address => bool)) public signatures;
103:    mapping(bytes32 => uint256) public signatureCount;
120:    mapping(address => PendingRelease[]) public pendingReleasesByRecipient;
126:    mapping(address => bool) public hasPendingReleases;

Token.sol
25:    mapping (address => uint256) public override balanceOf;
26:    mapping (address => mapping (address => uint256)) public override allowance;
```

**BridgeX:**
Fixed in commit [43b99ff](https://github.com/NerdUnited-NodeGovernance/audit-2026-03-bridgex/commit/43b99ff62021c64bf214a6bf213ec8a8b9d19314).

**Cyfrin:** Verified.
