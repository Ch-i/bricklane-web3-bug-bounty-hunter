---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-16-cyfrin-accountable-v2-0-2-2
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-10-16T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-16-cyfrin-accountable-v2-0
title: '`AccountableAsyncRedeemVault` allows deposits for non-whitelisted or non-KYCed
  addresses'
vuln_class: []
---

# `AccountableAsyncRedeemVault` allows deposits for non-whitelisted or non-KYCed addresses

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-16-cyfrin-accountable-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md)_

---

**Description:** Almost all functions in `AccountableAsyncRedeemVault` use an `onlyAuth()` modifier to verify that the caller is KYC-ed or Whitelisted (according to the vault's own policy).

This logic can be seen in `isVerified()` function in AccessBase.sol

Here is the `AccountableAsyncRedeemVault::onlyAuth` modifier :

```solidity
    modifier onlyAuth() {
        if (!isVerified(msg.sender, msg.data)) revert Unauthorized();
        _;
    }

```

This passes `msg.sender` as the "Account" address to be verified, but these checks are not working.

If we look at the `deposit()` function here, `msg.sender` is not the actual account address, for whom the deposit will be done, instead the "receiver" address here is the actual account. The "Receiver" address receives the shares but it is not verified that they are whitelisted/ KYC-ed.

```solidity
    function deposit(uint256 assets, address receiver, address controller) public onlyAuth returns (uint256 shares) {
        _checkController(controller);
        if (assets == 0) revert ZeroAmount();
        if (assets > maxDeposit(controller)) revert ExceedsMaxDeposit();

        uint256 price = strategy.onDeposit(address(this), assets, receiver, controller);
        shares = _convertToShares(assets, price, Math.Rounding.Floor);

        _mint(receiver, shares);
        _deposit(controller, assets);

```

This means that a KYC'ed user can call `deposit()` and mint new share tokens for random "receiver" addresses (who have set the KYC'ed user as their operator using `setOperator()` and for the input params `controller == receiver` can be used). This "receiver" can then take part in the vault by holding vault shares, redeeming them via the operator etc.

**Impact:** The KYC/ Whitelist configuration does not prevent KYC’ed addresses from minting shares to non-KYCed addresses.

Similar problems might exist in the access control for other methods in the vault, the reason being `onlyAuth()` only checks the msg.sender and not the other address holding the position.

**Recommended Mitigation:** Consider documenting what is the intended permissions granted to a KYC-ed/ Whitelisted user. If they should not be allowed to open positions for other non KYC-ed addresses, then the auth checks need to be done for actual receiver/ controller addresses.

**Accountable:** Fixed in commits [`c804a31`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/c804a31d3e5b161065b775fa57f3590be3581e5a) and [`2eeb273`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/2eeb2736eb5ba8dafa2c9f2f458b31fd8eb2d6bf)

**Cyfrin:** Verified. Both `reciever` and `controller` are verified to be KYC'd throughout the calls.
