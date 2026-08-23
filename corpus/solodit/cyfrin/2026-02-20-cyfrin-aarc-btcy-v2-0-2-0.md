---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-20-cyfrin-aarc-btcy-v2-0-2-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-02-20T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-20-cyfrin-aarc-btcy-v2-0
title: Use named mappings to explicitly indicate the purpose of keys and values
vuln_class: []
---

# Use named mappings to explicitly indicate the purpose of keys and values

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-20-cyfrin-aarc-btcy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md)_

---

**Description:** Use named mappings to explicitly indicate the purpose of keys and values:
```solidity
base/AllowList.sol
26:        mapping(address => bool) allowlistedAddresses;

Pricer.sol
57:        mapping(uint256 => PriceInfo) prices;

IBTCYHub.sol
104:        mapping(bytes32 => Depositor) depositIdToDepositor;
106:        mapping(bytes32 => Redeemer) redemptionIdToRedeemer;

BTCY.sol
56:        mapping(address => bool) transferDenylisted;

DepositWithdraw.sol
50:    mapping(address => bool) private _whitelistedTokens;
53:    mapping(address => bool) private _whitelistedUsers;
```

**Aarc:** Fixed in commit [50e7b72](https://github.com/aarc-xyz/btcy-contracts-main/commit/50e7b72b194abdd317e13f7625a2b7d14a69c411).

**Cyfrin:** Verified.
