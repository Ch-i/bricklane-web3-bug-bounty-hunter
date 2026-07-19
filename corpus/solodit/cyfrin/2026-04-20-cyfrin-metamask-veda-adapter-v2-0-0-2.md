---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-20-cyfrin-metamask-veda-adapter-v2-0-0-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-04-20T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-20-cyfrin-metamask-veda-adapter-v2.0.md
tags:
- firm:cyfrin
- report:2026-04-20-cyfrin-metamask-veda-adapter-v2-0
title: '`VedaAdapter` acts as a shared `msg.sender` for all Teller withdrawals, allowing
  any entity authorized for the `TellerWithMultiAssetSupport::deposit` to lock the
  adapter and block all user withdrawals'
vuln_class: []
---

# `VedaAdapter` acts as a shared `msg.sender` for all Teller withdrawals, allowing any entity authorized for the `TellerWithMultiAssetSupport::deposit` to lock the adapter and block all user withdrawals

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-20-cyfrin-metamask-veda-adapter-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-20-cyfrin-metamask-veda-adapter-v2.0.md)_

---

**Description:** The Veda Teller's `withdraw` function enforces a share lock check against `msg.sender`:

```solidity
// TellerWithMultiAssetSupport.sol:558-568
function withdraw(ERC20 withdrawAsset, uint256 shareAmount, uint256 minimumAssets, address to)
    external
    virtual
    requiresAuth
    nonReentrant
    returns (uint256 assetsOut)
{
    beforeTransfer(msg.sender, address(0), msg.sender); // @audit - checks VedaAdapter's lock, not the user's
    assetsOut = _withdraw(withdrawAsset, shareAmount, minimumAssets, to);
    ...
}
```
The `beforeTransfer` hook reverts if the `from` address has a non-expired share lock:

```solidity
// TellerWithMultiAssetSupport.sol:378-388
function beforeTransfer(address from, address to, address operator) public view virtual {
    ...
    if (beforeTransferData[from].shareUnlockTime > block.timestamp) { // @audit - from = VedaAdapter
        revert TellerWithMultiAssetSupport__SharesAreLocked();
    }
}
```
When `VedaAdapter` calls `teller.withdraw()`, `msg.sender` is the adapter contract itself — shared across all users. Meanwhile, the 5-arg `deposit()` sets the share lock on an arbitrary `to` address:

```solidity
// TellerWithMultiAssetSupport.sol:482-490
function deposit(
    ERC20 depositAsset, uint256 depositAmount, uint256 minimumMint,
    address to, // @audit - can be set to VedaAdapter's address
    address referralAddress
) external payable virtual requiresAuth nonReentrant returns (uint256 shares) {
    shares = _publicDeposit(depositAsset, depositAmount, minimumMint, to, referralAddress);
}
```

Which ultimately sets the lock:

```solidity
// TellerWithMultiAssetSupport.sol:664
beforeTransferData[user].shareUnlockTime = block.timestamp + currentShareLockPeriod; // @audit - user = VedaAdapter
```

If any entity authorized for the 5-arg `TellerWithMultiAssetSupport::deposit()` selector calls `teller.deposit(token, 1, 0, vedaAdapterAddress, address(0))`, the adapter's `shareUnlockTime` is set, and every subsequent `teller.withdraw()` called by the adapter reverts for all users until the lock expires.

The root cause is a design mismatch: the Teller's share lock was built for direct user interactions where the depositor and withdrawer are the same `msg.sender`. The `VedaAdapter` breaks this assumption by acting as a shared intermediary, turning a per-user lock into a global lock surface.


**Impact:** If any entity besides `VedaAdapter` is authorized for the 5-arg `deposit()` selector on the Teller (or if it is made public), an attacker can:
- Block **all** withdrawals through `VedaAdapter` for up to `shareLockPeriod`
- Repeat the 1 wei deposit before each lock expiry to maintain an **indefinite DoS** on all adapter withdrawals
- Cost per lock period: 1 wei of any allowed deposit asset

All users who deposited through the adapter are unable to withdraw their funds for the duration of the attack.


**Recommended Mitigation:** Ensure the 5-arg `TellerWithMultiAssetSupport::deposit()` selector is restricted exclusively to the `VedaAdapter` in the RolesAuthority configuration, with no other entity sharing the role. This is an operational mitigation, not a code fix.

Alternatively keep a low enough `shareLockPeriod`, `0` (disabled), or a couple of seconds to ensure flash deposit/withdrawals cannot be done.

**Metamask:**
Acknowledged: VedaVault will limit to VedaAdapter for deposit call with `to` parameter.

\clearpage
