---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-22-cyfrin-remora-dynamic-tokens-v2-1-4-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-10-22T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-22-cyfrin-remora-dynamic-tokens-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-22-cyfrin-remora-dynamic-tokens-v2-1
title: Admin could use `CentralToken::transferFrom` after approval to break 1:1 invariant
  in child token
vuln_class: []
---

# Admin could use `CentralToken::transferFrom` after approval to break 1:1 invariant in child token

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-22-cyfrin-remora-dynamic-tokens-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-22-cyfrin-remora-dynamic-tokens-v2.1.md)_

---

**Description:** Function `transfer` contains `_checkAllowedAdmin(to)` which prevents an admin (accidentally or otherwise) sending a `CentralToken` to a `ChildToken` directly.

```solidity
    function transfer(address to, uint256 amount) public override returns (bool) {
        if (amount == 0) return true;
        _checkAllowedAdmin(to);
        return super.transfer(to, amount);
    }
```

However, `transferFrom` is not overridden so it is possible for an admin to:
- `approve` the `CentralToken` contract
- call `transferFrom(address(this), childToken, amount)` (for some `childToken` and `amount`)

This will immediately brick the `ChildToken` contract from minting since `mint` contains this check:

```solidity
function mint(address to, uint256 amount) external whenNotPaused {
...
        if(ICentralToken(cToken).balanceOf(address(this)) != totalSupply() + amount)
            revert CentralBalanceInvariant();
```

**Impact:** An admin's transfer can permanently disabled `CentralToken::dynamicTransfer` being called when it would send tokens to the `ChildToken` with the broken invariant.

Further, the directly-transferred token could not be recovered using `ChildToken::burn` since it never had a `ChildToken` minted for it.

**Proof of Concept:** Add this test to `CentralTokenTest.t.sol`

```solidity
function test_cyfrin_brickMintingInChildToken() public {
    address dom = getDomesticUser(0);
    centralTokenProxy.mint(address(this), uint64(4));

    // send 1 token to the child contract directly, after approving
    centralTokenProxy.approve(address(this), type(uint256).max);
    centralTokenProxy.transferFrom(address(this), address(d_childTokenProxy), 1);

    vm.expectRevert(bytes4(keccak256("CentralBalanceInvariant()")));
    centralTokenProxy.dynamicTransfer(dom, 3);
}
```

**Recommended Mitigation:**
1. Override `transferFrom` with the following definition

```solidity
function transferFrom(address from, address to, uint256 amount) public override returns (bool) {
    if (amount == 0) return true;
    _checkAllowedAdmin(to);
    return super.transferFrom(from, to, amount);
}
```

2. It may also be worth disabling the `approve` function if it is not strictly needed

3. It may also be worth updating `Allowlist.addUser` to check whether a user's address is a contract, or if you want to allow contracts, checking that it doesn't satisfy the interface of `ChildToken`

**Remora:** Fixed at commit [2fc2c11](https://github.com/remora-projects/remora-dynamic-tokens/commit/2fc2c119b8cec8f46ccd9bacf5cb9ead1c040484).

**Cyfrin:** Verified. `transfer()` and `transferFrom()` are overridden, and a validation was added to prevent the recipient from being a ChildToken.
