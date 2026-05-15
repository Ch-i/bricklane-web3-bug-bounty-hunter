---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-16-cyfrin-accountable-v2-0-2-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-10-16T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-16-cyfrin-accountable-v2-0
title: '`transferWhitelist` checks are missing in `AccountableVault::_checkTransfer`'
vuln_class: []
---

# `transferWhitelist` checks are missing in `AccountableVault::_checkTransfer`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-16-cyfrin-accountable-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md)_

---

**Description:** AccountableVault.sol employs a "transferWhitelist" feature to help select addresses that should be allowed to transfer vault shares, overriding the other restrictions checked in `_checkTransfer()`.

Both `transfer()` and `transferFrom()` functions internally call `_checkTransfer()`, but the "transferWhitelist" check is missing in all transfer flows.

**Impact:** The transferWhitelist feature does not work, so it does not make a difference if an address was whitelisted or not.

```solidity
    /// @notice Mapping of addresses that can override transfer restrictions
    mapping(address => bool) public transferWhitelist;
```

The comment above says "Mapping of addresses that can override transfer restrictions" which does not hold true as transferWhitelist is never being checked.

A method to call vault.setTransferWhitelist() is also missing in both the current strategy contracts, so when fixing keep note of it.

**Recommended Mitigation:**
```solidity
    function _checkTransfer(uint256 amount, address from, address to) private {

+++      if(transferWhitelist[from] && transferWhitelist[to]) return;

        if (amount == 0) revert ZeroAmount();
        if (!transferableShares) revert SharesNotTransferable();
        if (!isVerified(to, msg.data)) revert Unauthorized();
        if (throttledTransfers[from] > block.timestamp) revert TransferCooldown();
    }
```

Also consider adding a method to the AccountableFixedTerm and AccountableOpenTerm strategy contracts (one that calls vault.setTransferWhitelist()) if it is required in context of that strategy.

**Accountable:** Whitelist removed in commit [`6a81e38`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/6a81e389513ad690216fc8c037ec69513f3121c7)

**Cyfrin:** Verified. Whitelist removed.
