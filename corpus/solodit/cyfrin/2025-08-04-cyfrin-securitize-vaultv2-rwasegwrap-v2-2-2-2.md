---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2-2-2-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-08-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md
tags:
- firm:cyfrin
- report:2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2-2
title: Redundant balance check in safeTransferFrom before calling underlying transfer
  function
vuln_class: []
---

# Redundant balance check in safeTransferFrom before calling underlying transfer function

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md)_

---

**Description:** The `RWASegWrap::safeTransferFrom()` function performs an unnecessary balance check on lines 452-454 before calling the underlying transfer function:

```solidity
uint256 currentBalance = balanceOf(from, id);
if (currentBalance < value) {
    revert ERC1155InsufficientBalance(from, currentBalance, value, id);
}
```

This balance check is redundant because the subsequent call to `ISegregatedVault(vaults[id]).internalTransferFrom(from, to, _msgSender(), value)` internally calls the ERC20 `_transfer()` function, which already performs the same balance validation. The ERC20 `_update()` function (which `_transfer()` calls) contains the exact same check:

```solidity
uint256 fromBalance = $._balances[from];
if (fromBalance < value) {
    revert ERC20InsufficientBalance(from, fromBalance, value);
}
```

When the balance is insufficient, the ERC20 mechanism will automatically revert with `ERC20InsufficientBalance`, making the wrapper-level balance check redundant.

**Impact:** The redundant balance check results in unnecessary gas consumption and code complexity without providing additional safety.

**Recommended Mitigation:** Remove the redundant balance check:

```diff
function safeTransferFrom(
    address from,
    address to,
    uint256 id,
    uint256 value,
    bytes memory data
) public virtual override whenNotPaused idNotZero(id) recognizedVault(id) {
    if (to == address(0)) {
        revert ERC1155InvalidReceiver(address(0));
    }
    if (from == address(0)) {
        revert ERC1155InvalidSender(address(0));
    }
    uint256 vaultId = getVaultId(from);
    if (id != vaultId) {
        revert InvestorVaultMismatch(id, from);
    }

    uint256 currentAllowance = allowance(from, _msgSender(), id);
    if (currentAllowance < value) {
        revert ERC1155MissingApprovalForAll(_msgSender(), from);
    }

-   uint256 currentBalance = balanceOf(from, id);
-   if (currentBalance < value) {
-       revert ERC1155InsufficientBalance(from, currentBalance, value, id);
-   }

    emit TransferSingle(_msgSender(), from, to, id, value);
    ISegregatedVault(vaults[id]).internalTransferFrom(from, to, _msgSender(), value);
    ERC1155Utils.checkOnERC1155Received(_msgSender(), from, to, id, value, data);
}
```

**Securitize:** Fixed in commit [13955e](https://github.com/securitize-io/bc-rwa-seg-wrap-sc/commit/13955e2b094b19d8bfb71020498c4607c127627f).

**Cyfrin:** Verified.
