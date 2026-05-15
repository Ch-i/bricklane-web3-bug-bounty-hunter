---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-01-cyfrin-licredity-v2-0-4-3
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-09-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-01-cyfrin-licredity-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-01-cyfrin-licredity-v2-0
title: Missing zero address check in Uniswap modules initialization
vuln_class: []
---

# Missing zero address check in Uniswap modules initialization

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-01-cyfrin-licredity-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-01-cyfrin-licredity-v2.0.md)_

---

**Description:** The `initialize` function in `UniswapV3ModuleLibrary` does not check if `poolFactory` or `positionManager` are the zero address. If `poolFactory` is set to `address(0)`, the module can be reinitialized, since the only protection against reinitialization is `require(address(self.poolFactory) == address(0), AlreadyInitialized());`. This allows an attacker or a bug to reset the module's configuration, which is not intended.

Similarly, the `initialize` function in `UniswapV4ModuleLibrary` does not check if `poolManager` or `positionManager` are the zero address. If `poolManager` is set to `address(0)`, the module can be reinitialized, since the only protection against reinitialization is `require(address(self.poolManager) == address(0), AlreadyInitialized());`. This allows an attacker or a bug to reset the module's configuration, which is not intended.

**Impact:** The modules can be reinitialized with new parameters if `poolFactory`/`poolManager` is set to zero, breaking immutability guarantees. This could lead to loss of control over the modules, misconfiguration, or security issues if the module is pointed to malicious contracts. Denial of service may occur if critical addresses are set to zero.

**Recommended Mitigation:** Add explicit checks to ensure that neither `poolFactory`/`poolManager` nor `positionManager` are the zero address during initialization. For example:

```solidity
require(poolFactory != address(0) && positionManager != address(0), "UniswapV3Module: zero address");
```

and

```solidity
require(poolManager != address(0) && positionManager != address(0), "UniswapV4Module: zero address");
```

This prevents accidental or malicious reinitialization and enforces proper configuration.

**Licredity:** Fixed in [PR#15](https://github.com/Licredity/licredity-v1-oracle/pull/15/files), commits, [`21e5396`](https://github.com/Licredity/licredity-v1-oracle/commit/21e539657d20317fa8b874c20884a86fec807130), [`bd56d24`](https://github.com/Licredity/licredity-v1-oracle/commit/bd56d246e2eed497288b82f0281ccf76fe5d4e7d), and [`d0845ae`](https://github.com/Licredity/licredity-v1-oracle/commit/d0845aed9451a7d1c7267cb2238f78965094373b)

**Cyfrin:** Verified. Initialize function now only takes positionManager, makes sure itself wasn't already initialized and use it to get associated factory / pool manager.
