---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-bridgex-v2-0-3-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-bridgex-v2-0
title: Use `immutable` variables for non-upgradeable contracts whose storage is only
  set once in the constructor
vuln_class: []
---

# Use `immutable` variables for non-upgradeable contracts whose storage is only set once in the constructor

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-bridgex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md)_

---

**Description:** Use `immutable` variables for non-upgradeable contracts whose storage is only set once in the constructor:
* `PublicBridge::TokenVault::bridge, token`
* `PublicBridge::token, vault`
* `PrivateChainBridge::TokenVault::bridge`
* `PrivateChainBridge::vault`
* `Token::maxSupply, decimals`

**BridgeX:**
Fixed in commits [0917ee5](https://github.com/NerdUnited-NodeGovernance/audit-2026-03-bridgex/commit/0917ee5359db3171c9bd4a4518f0bb3b52e8c5cd), [32882e0](https://github.com/NerdUnited-NodeGovernance/bridge-x-contracts/commit/32882e07d78a39d435db99c46950ca286687dca1).

**Cyfrin:** Verified.
