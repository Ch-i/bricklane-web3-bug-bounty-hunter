---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-11-cyfrin-securitize-evm-globaldenylist-v2-0-1-2
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-09-11T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-11-cyfrin-securitize-evm-globaldenylist-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-11-cyfrin-securitize-evm-globaldenylist-v2-0
title: Denylist mutators always return `true`, discarding the `EnumerableSet` result
vuln_class: []
---

# Denylist mutators always return `true`, discarding the `EnumerableSet` result

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-11-cyfrin-securitize-evm-globaldenylist-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-11-cyfrin-securitize-evm-globaldenylist-v2.0.md)_

---

**Description:** [`addToGlobalDenylist`](https://github.com/securitize-io/bc-global-denylist-manager-sc/blob/main/bc-global-denylist-manager-sc/contracts/denylist/GlobalDenyListManager.sol#L105-L108) and [`removeFromGlobalDenylist`](https://github.com/securitize-io/bc-global-denylist-manager-sc/blob/main/bc-global-denylist-manager-sc/contracts/denylist/GlobalDenyListManager.sol#L111-L114) end in a literal `return true`:

```solidity
function addToGlobalDenylist(address wallet) external override onlyRole(OPERATOR_ROLE) whenNotPaused addressNotZero(wallet) returns (bool) {
    _addToGlobalDenylist(wallet);
    return true;
}
```

`EnumerableSet.add` returns true only if the wallet was not already present, and `.remove` only if it was present.

The interface asks for the opposite of a constant: [IGlobalDenyListManager.sol:113](https://github.com/securitize-io/bc-global-denylist-manager-sc/blob/main/bc-global-denylist-manager-sc/contracts/denylist/IGlobalDenyListManager.sol#L113) and [:121](https://github.com/securitize-io/bc-global-denylist-manager-sc/blob/main/bc-global-denylist-manager-sc/contracts/denylist/IGlobalDenyListManager.sol#L121) declare `@return True on success`. A no-op — adding an already-denylisted wallet, removing one that was never listed — emits no event and returns `true`, indistinguishable from a call that changed the set. Since there is no enumeration getter, the return is the caller's only per-call signal, and it carries no information.

**Recommended Mitigation:** Return the helper's result. Event behaviour is unchanged:

```solidity
function addToGlobalDenylist(address wallet) external override onlyRole(OPERATOR_ROLE) whenNotPaused addressNotZero(wallet) returns (bool) {
    return _addToGlobalDenylist(wallet);
}

function _addToGlobalDenylist(address wallet) private returns (bool added) {
    added = _globallyDenylistedWallets.add(wallet);
    if (added) {
        emit WalletAddedToGlobalDenylist(wallet, _msgSender());
    }
}
```

Same for `removeFromGlobalDenylist`. Update the NatSpec to `@return True if the wallet was newly added, false if it was already denylisted` (and the mirror for removal). For the bulk functions, either return the count of wallets actually changed or document that the `bool` is always `true`.

**Securitize:** Fixed in commit [98c9a3a](https://github.com/securitize-io/bc-global-denylist-manager-sc/commit/98c9a3ab8b9a23c57f338828f6bd9f535443b9b4).

**Cyfrin:** Verified.
