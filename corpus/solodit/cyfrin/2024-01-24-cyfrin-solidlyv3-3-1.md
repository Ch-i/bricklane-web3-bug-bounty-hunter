---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-01-24-cyfrin-solidlyv3-3-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-01-24T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-24-cyfrin-solidlyV3.md
tags:
- firm:cyfrin
- report:2024-01-24-cyfrin-solidlyv3
title: Don't initialize variables with default value
vuln_class: []
---

# Don't initialize variables with default value

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-01-24-cyfrin-solidlyV3.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-24-cyfrin-solidlyV3.md)_

---

**Description:** Don't initialize variables with default value:

```solidity
File: contracts/RewardsDistributor.sol

184:         for (uint256 i = 0; i < numClaims; ) {

```

```solidity
File: libraries/TickMath.sol

67:         uint256 msb = 0;

```

**Solidly:**
Fixed in commit [6481747](https://github.com/SolidlyV3/v3-rewards/commit/6481747737b98c8650a36f87b1aeace815505ba9) for `RewardsDistributor`; v3-core is already deployed and not upgradeable.

**Cyfrin:**
Verified.
