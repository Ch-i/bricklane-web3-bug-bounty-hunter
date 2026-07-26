---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-dolomite-polvaults-v2-0-3-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-04-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-dolomite-POLVaults-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-24-cyfrin-dolomite-polvaults-v2-0
title: Inconsistent ETH handling pattern in Proxy Contracts
vuln_class: []
---

# Inconsistent ETH handling pattern in Proxy Contracts

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-dolomite-POLVaults-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-dolomite-POLVaults-v2.0.md)_

---

**Description:** There is an inconsistency in how proxy contracts handle incoming ETH transactions through their `receive()` and `fallback()` functions. Some proxy contracts delegate both functions to their implementation, while others only delegate the fallback() function while leaving the receive() function empty.

For example, in `MetaVaultUpgradeableProxy.sol`, both functions delegate:

```solidity
// MetaVaultUpgradeableProxy
receive() external payable requireIsInitialized {
    _callImplementation(implementation());
}

fallback() external payable requireIsInitialized {
    _callImplementation(implementation());
}
```

Whereas in `POLIsolationModeWrapperUpgradeableProxy.sol`  and `POLIsolationModeUnwrapperUpgradeableProxy`, only the `fallback()` function delegates:

```solidity
// POLIsolationModeWrapperUpgradeableProxy
receive() external payable {} // solhint-disable-line no-empty-blocks

fallback() external payable {
    _callImplementation(implementation());
}
```

While this is a design choice and not a security issue per se, it could lead to potential confusion among developers who might expect all proxies to handle ETH transfers in a similar manner.

**Recommended Mitigation:** Consider documenting the chosen approach and reasoning in the contract comments to clarify the intended behavior for other developers.

**Dolomite:** Fixed [d4ceeef](https://github.com/dolomite-exchange/dolomite-margin-modules/commit/d4ceeefc9c2a5b8c51c8ea77512e499a2e0bc811).

**Cyfrin:** Verified.
