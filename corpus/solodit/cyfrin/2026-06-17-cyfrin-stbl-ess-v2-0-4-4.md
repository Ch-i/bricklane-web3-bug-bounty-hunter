---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-17-cyfrin-stbl-ess-v2-0-4-4
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-06-17T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-17-cyfrin-stbl-ess-v2-0
title: UUPS implementation contracts omit `_disableInitializers()`
vuln_class: []
---

# UUPS implementation contracts omit `_disableInitializers()`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-17-cyfrin-stbl-ess-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md)_

---

**Description:** Four of the upgradeable contracts leave their implementation (logic) contract directly initializable because their constructors do not call `_disableInitializers()`. `STBL_XLayer_Wrapper`, `STBL_XLayer_NFT_Vault`, `STBL_XLayer_Asset_Issuer`, and `STBL_XLayer_Asset_Vault` all have a constructor of the form:

```solidity
constructor() ERC2771ContextUpgradeable(address(0)) {}
```

By contrast `STBL_XLLayer_Token` does it correctly:

```solidity
constructor() ERC2771ContextUpgradeable(address(0)) {
    _disableInitializers();
}
```

Without `_disableInitializers()`, anyone can call `initialize` directly on the deployed implementation contract and become its admin or `UPGRADER_ROLE` holder.

This is best-practice hardening rather than a live exploit. Initializing the implementation does not affect the proxy, because the proxy holds its own independent storage. The classic escalation, calling `upgradeToAndCall` on the implementation to `selfdestruct` it and brick proxies, no longer works on post-Dencun chains because EIP-6780 restricts `selfdestruct` to contracts created in the same transaction. The proxies in scope are also already protected by `_authorizeUpgrade` checks that consult the registry or wrapper roles, so a hijacked implementation cannot upgrade a live proxy. No current runtime fund loss or DoS path exists.

**Impact:** Defense-in-depth gap only. An attacker can take ownership of the unused implementation contracts, which has no effect on the proxies or user funds on a post-Dencun chain. Informational.

**Recommended Mitigation:** Add `_disableInitializers()` to the constructor of `STBL_XLayer_Wrapper`, `STBL_XLayer_NFT_Vault`, `STBL_XLayer_Asset_Issuer`, and `STBL_XLayer_Asset_Vault`, matching `STBL_XLLayer_Token`:

```solidity
constructor() ERC2771ContextUpgradeable(address(0)) {
    _disableInitializers();
}
```

**STBL:** Fixed in commit [591d242](https://github.com/USD-Pi-Protocol/stbl-contracts-evm-ess-common/commit/591d2427cc5d7aab1e97270190061715ce41c735).

**Cyfrin:** Verified. All four affected UUPS implementation contracts — `STBL_XLayer_Wrapper`, `STBL_XLayer_NFT_Vault`, `STBL_XLayer_Asset_Issuer`, and `STBL_XLayer_Asset_Vault` — have been updated to call `_disableInitializers` in their constructors, matching the already-correct pattern in `STBL_XLayer_Token`.
