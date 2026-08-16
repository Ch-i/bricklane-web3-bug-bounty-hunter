---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2-2-2-4
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-08-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md
tags:
- firm:cyfrin
- report:2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2-2
title: Code duplication in function overrides that only add modifiers
vuln_class: []
---

# Code duplication in function overrides that only add modifiers

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md)_

---

**Description:** The `SecuritizeRWASegWrap` contract overrides four functions from its parent `RWASegWrap` contract (`deposit`, `redeem`, `redeemById`, and `depositById`) with identical implementation logic, only adding the `receiverIsSender` modifier. Instead of duplicating the entire function body, these functions should call their parent implementations using `super` after applying the additional modifier.

The current implementations in `SecuritizeRWASegWrap::deposit`, `SecuritizeRWASegWrap::redeem`, `SecuritizeRWASegWrap::redeemById`, and `SecuritizeRWASegWrap::depositById` repeat the exact same business logic as their parent functions in `RWASegWrap`, including variable declarations, vault resolution, validation checks, and internal function calls.

```solidity
// Current implementation in SecuritizeRWASegWrap
function deposit(uint256 assets, address receiver)
    public override whenNotPaused amountNotZero(assets) addressNotZero(receiver) receiverIsSender(receiver)
    returns (uint256) {
    address caller = _msgSender();
    uint256 vaultId = getVaultId(caller);
    if (vaultId == 0) {
        vaultId = ++latestVaultId;
        vault = _deployVault(vaultId);
        _addVault(address(vault), vaultId, caller);
    }
    return _doDeposit(caller, assets, receiver, vaultId);
}

// Parent implementation in RWASegWrap (identical logic except missing receiverIsSender modifier)
function deposit(uint256 assets, address receiver)
    external virtual override whenNotPaused amountNotZero(assets) addressNotZero(receiver)
    returns (uint256) {
    address caller = _msgSender();
    uint256 vaultId = _resolveVaultId(caller);
    return _doDeposit(caller, assets, receiver, vaultId);
}
```

**Impact:** This code duplication increases the maintenance burden while creating a risk of inconsistencies.

**Recommended Mitigation:** Refactor the overridden functions to use `super` calls instead of duplicating logic:

```diff
function deposit(uint256 assets, address receiver)
    public override whenNotPaused amountNotZero(assets) addressNotZero(receiver) receiverIsSender(receiver)
    returns (uint256) {
-   address caller = _msgSender();
-   uint256 vaultId = getVaultId(caller);
-   if (vaultId == 0) {
-       vaultId = ++latestVaultId;
-       vault = _deployVault(vaultId);
-       _addVault(address(vault), vaultId, caller);
-   }
-   return _doDeposit(caller, assets, receiver, vaultId);
+   return super.deposit(assets, receiver);
}

function redeem(uint256 shares, address receiver, address owner)
    external override whenNotPaused amountNotZero(shares) addressNotZero(receiver) receiverIsSender(receiver) addressNotZero(owner)
    returns (uint256) {
-   address caller = _msgSender();
-   uint256 vaultId = getVaultId(caller);
-   if (vaultId == 0) {
-       revert VaultNotFound();
-   }
-   return _doRedeem(caller, shares, receiver, owner, vaultId);
+   return super.redeem(shares, receiver, owner);
}

function redeemById(uint256 shares, address receiver, address owner, uint256 id)
    external override whenNotPaused amountNotZero(shares) addressNotZero(receiver) addressNotZero(owner) receiverIsSender(receiver) idNotZero(id) recognizedVault(id)
    returns (uint256) {
-   address caller = _msgSender();
-   uint256 vaultId = getVaultId(caller);
-   if (id != vaultId) {
-       revert InvestorVaultMismatch(id, caller);
-   }
-   return _doRedeem(caller, shares, receiver, owner, id);
+   return super.redeemById(shares, receiver, owner, id);
}

function depositById(uint256 assets, address receiver, uint256 id)
    external override whenNotPaused amountNotZero(assets) receiverIsSender(receiver) idNotZero(id) recognizedVault(id)
    returns (uint256) {
-   address caller = _msgSender();
-   uint256 vaultId = getVaultId(caller);
-   if (id != vaultId) {
-       revert InvestorVaultMismatch(id, caller);
-   }
-   return _doDeposit(caller, assets, receiver, vaultId);
+   return super.depositById(assets, receiver, id);
}
```

**Securitize:** Fixed in commit [6322e3](https://github.com/securitize-io/bc-rwa-seg-wrap-sc/commit/6322e36c86c012123db32e3dcd6cfe9ebd99eed4).

**Cyfrin:** Verified.

\clearpage
