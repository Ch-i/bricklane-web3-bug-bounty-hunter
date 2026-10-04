---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-11-cyfrin-securitize-evm-globaldenylist-v2-0-2-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-09-11T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-11-cyfrin-securitize-evm-globaldenylist-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-11-cyfrin-securitize-evm-globaldenylist-v2-0
title: Cache identical storage reads in `ComplianceServicePermissionless::_isGloballyDenylisted,
  _isLocallyBlacklisted`
vuln_class: []
---

# Cache identical storage reads in `ComplianceServicePermissionless::_isGloballyDenylisted, _isLocallyBlacklisted`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-11-cyfrin-securitize-evm-globaldenylist-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-11-cyfrin-securitize-evm-globaldenylist-v2.0.md)_

---

**Description:** `ComplianceServicePermissionless::_isGloballyDenylisted` reads `services[GLOBAL_DENYLIST_MANAGER]` twice per call: once directly through `ServiceConsumer::getDSService` for the `address(0)` guard, then again inside `ServiceConsumer::getGlobalDenyListManager`, which is itself a `getDSService` wrapper. `ComplianceServicePermissionless::_isLocallyBlacklisted` has the identical shape against `services[BLACKLIST_MANAGER]`. Each redundant read costs a warm `SLOAD`, a recomputed `keccak256` mapping-slot derivation, and an internal dispatch.

`ComplianceServicePermissionless::checkTransfer` multiplies the waste: it calls each helper once for `_from` and once for `_to`, so a passing transfer performs eight reads of only two distinct storage slots. `checkTransfer` is on the state-changing path of every transfer via `ComplianceService::validateTransfer`, so the cost is borne by every token holder. `ComplianceServicePermissionless::preIssuanceCheck` and `ComplianceServicePermissionless::getComplianceTransferableTokens` call the same helpers and inherit the per-call redundancy.

The address cannot go stale between reads. `services` is written only by `ServiceConsumer::setDSService`, which is `onlyMaster`, and the interposed `IDSGlobalDenyListManager::isGloballyDenylisted` and `IDSBlackListManager::isBlacklisted` calls are declared `view`, so the compiler emits `STATICCALL` and no reentrant write is reachable.

**Impact:** Measured with a `solc` 0.8.22 harness (optimizer on, runs 200) reproducing the exact call shape against `view` manager mocks, on the passing path where neither wallet is listed:

- caching inside both helpers alone saves 507 gas per transfer
- caching plus a two-wallet form for `checkTransfer` saves 886 gas per transfer

**Recommended Mitigation:** Cache the resolved manager address in a local and reuse it. First fix both helpers in place, so every caller benefits:

```solidity
function _isGloballyDenylisted(address _wallet) internal view returns (bool) {
    address manager = getDSService(GLOBAL_DENYLIST_MANAGER);
    if (manager == address(0)) return false;
    return IDSGlobalDenyListManager(manager).isGloballyDenylisted(_wallet);
}

function _isLocallyBlacklisted(address _wallet) internal view returns (bool) {
    address manager = getDSService(BLACKLIST_MANAGER);
    if (manager == address(0)) return false;
    return IDSBlackListManager(manager).isBlacklisted(_wallet);
}
```

Then add two-wallet variants so `checkTransfer` resolves each manager once for both wallets:

```solidity
function _anyGloballyDenylisted(address _a, address _b) internal view returns (bool) {
    address manager = getDSService(GLOBAL_DENYLIST_MANAGER);
    if (manager == address(0)) return false;
    IDSGlobalDenyListManager denyList = IDSGlobalDenyListManager(manager);
    return denyList.isGloballyDenylisted(_a) || denyList.isGloballyDenylisted(_b);
}

function _anyLocallyBlacklisted(address _a, address _b) internal view returns (bool) {
    address manager = getDSService(BLACKLIST_MANAGER);
    if (manager == address(0)) return false;
    IDSBlackListManager blackList = IDSBlackListManager(manager);
    return blackList.isBlacklisted(_a) || blackList.isBlacklisted(_b);
}

function checkTransfer(
    address _from,
    address _to,
    uint256 /*_value*/
) internal view virtual override returns (uint256 code, string memory reason) {
    if (_anyGloballyDenylisted(_from, _to)) {
        return (102, WALLET_GLOBALLY_DENYLISTED);
    }

    if (_anyLocallyBlacklisted(_from, _to)) {
        return (100, WALLET_BLACKLISTED);
    }

    return (0, VALID);
}
```

This requires importing `IDSBlackListManager` and `IDSGlobalDenyListManager` into `ComplianceServicePermissionless`, since `ServiceConsumer` uses named imports and does not re-export them. Short-circuit ordering and the `address(0)` fail-open semantics are unchanged.

**Securitize:** Fixed in commit [92903ba](https://github.com/securitize-io/dstoken/commit/92903ba9b850720c2e5955f0e0bd27267d3bca3a).

**Cyfrin:** Verified.


\clearpage
