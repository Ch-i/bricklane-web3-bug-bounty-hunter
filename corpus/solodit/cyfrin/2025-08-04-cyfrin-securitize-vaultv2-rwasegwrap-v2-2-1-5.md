---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2-2-1-5
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-08-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md
tags:
- firm:cyfrin
- report:2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2-2
title: Incorrect allowance check in transfer functions prevents users from transferring
  their own tokens
vuln_class: []
---

# Incorrect allowance check in transfer functions prevents users from transferring their own tokens

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md)_

---

**Description:** The protocol implements transfer functions in both `RWASegWrap` and `SecuritizeRWASegWrap` contracts that violate standard token transfer practices by always checking allowance, even when users are transferring their own tokens.

In `RWASegWrap::safeTransferFrom()`, lines 448-450 always check the allowance:
```solidity
uint256 currentAllowance = allowance(from, _msgSender(), id);
if (currentAllowance < value) {
    revert ERC1155MissingApprovalForAll(_msgSender(), from);
}
```

Similarly, `RWASegWrap::transferFrom()` calls `ISegregatedVault(vaults[id]).internalTransferFrom(from, to, _msgSender(), value)` which internally calls `_spendAllowance(from, spender, value)` where the spender is `_msgSender()`, forcing an allowance check even for self-transfers.

According to standard token implementation practices, allowance checks should only occur when the sender is not the token owner. The correct behavior is demonstrated in OpenZeppelin's implementation, where approval is only checked when `from != sender`:

```solidity
// OpenZeppelin's ERC1155Upgradeable
address sender = _msgSender();
if (from != sender && !isApprovedForAll(from, sender)) {
    revert ERC1155MissingApprovalForAll(sender, from);
}
```

`SecuritizeRWASegWrap` inherits from `RWASegWrap` and therefore has the same non-compliant behavior for both transfer functions.

**Impact:** Users cannot transfer their own tokens without first calling approve to grant themselves allowance, creating unnecessary friction and violating standard token transfer expectations.

**Recommended Mitigation:** Modify the allowance check to only occur when the sender is not the token owner, following standard token implementation practices:

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

-   uint256 currentAllowance = allowance(from, _msgSender(), id);
-   if (currentAllowance < value) {
-       revert ERC1155MissingApprovalForAll(_msgSender(), from);
-   }
+   address sender = _msgSender();
+   if (from != sender) {
+       uint256 currentAllowance = allowance(from, sender, id);
+       if (currentAllowance < value) {
+           revert ERC1155MissingApprovalForAll(sender, from);
+       }
+   }

    uint256 currentBalance = balanceOf(from, id);
    if (currentBalance < value) {
        revert ERC1155InsufficientBalance(from, currentBalance, value, id);
    }

    emit TransferSingle(_msgSender(), from, to, id, value);
    ISegregatedVault(vaults[id]).internalTransferFrom(from, to, _msgSender(), value);
    ERC1155Utils.checkOnERC1155Received(_msgSender(), from, to, id, value, data);
}
```

The `internalTransferFrom` function should also be updated to conditionally call `_spendAllowance` only when `from != spender`.

**Securitize:** Fixed in commits [dd0035](https://github.com/securitize-io/bc-securitize-vault-sc/commit/dd0035fa0e700650b948191a70e7d6f9931a828e) and [4f0722](https://github.com/securitize-io/bc-rwa-seg-wrap-sc/commit/4f07223535989cc4fe99cfb22648a98addc61539).

**Cyfrin:** Verified.
