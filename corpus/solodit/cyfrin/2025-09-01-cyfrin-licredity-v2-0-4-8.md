---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-01-cyfrin-licredity-v2-0-4-8
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-09-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-01-cyfrin-licredity-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-01-cyfrin-licredity-v2-0
title: EIP-20 transfer functions accept zero address causing unintended token burns
vuln_class: []
---

# EIP-20 transfer functions accept zero address causing unintended token burns

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-01-cyfrin-licredity-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-01-cyfrin-licredity-v2.0.md)_

---

**Description:** EIP-20 compliance revealed that transfer() and transferFrom() accept the zero address as a recipient, which triggers token burning and causes unexpected totalSupply changes.

**Impact:** EIP-20 best practices.

**Proof of Concept:** :x:Violated: https://prover.certora.com/output/52567/a06b3c48627f41239d2cb1f7e0e237f6/?anonymousKey=38b44e833d45c5bf433d65284f2359cca844ae62

```solidity
// EIP20-05: Verify transfer() reverts in invalid conditions
// EIP-20: "The function SHOULD throw if the message caller's account balance does not have enough tokens to spend."
rule eip20_transferMustRevert(env e, address to, uint256 amount) {

    setup(e);

    // Snapshot the 'from' balance
    mathint fromBalancePrev = ghostERC20Balances128[_Licredity][e.msg.sender];

    // Attempt transfer with revert path
    transfer@withrevert(e, to, amount);
    bool reverted = lastReverted;

    assert(e.msg.sender == 0 => reverted,
           "[SAFETY] Transfer from zero address must revert");

    assert(to == 0 => reverted,
           "[SAFETY] Transfer to zero address must revert");

    assert(fromBalancePrev < amount => reverted,
           "[EIP-20] Transfer must revert if sender has insufficient balance");
}
```

**Recommended Mitigation:**
```diff
diff --git a/core/src/BaseERC20.sol b/core/src/BaseERC20.sol
index bed3880..5903415 100644
--- a/core/src/BaseERC20.sol
+++ b/core/src/BaseERC20.sol
@@ -56,6 +56,7 @@ abstract contract BaseERC20 is IERC20 {

     /// @inheritdoc IERC20
     function transfer(address to, uint256 amount) public returns (bool) {
+        require(to != address(0)); // @certora fix for eip20_transferMustRevert
         _transfer(msg.sender, to, amount);

         return true;
@@ -63,6 +64,7 @@ abstract contract BaseERC20 is IERC20 {

     /// @inheritdoc IERC20
     function transferFrom(address from, address to, uint256 amount) public returns (bool) {
+        require(to != address(0)); // @certora fix for eip20_transferFromMustRevert
         assembly ("memory-safe") {
             from := and(from, 0xffffffffffffffffffffffffffffffffffffffff)
```

:white_check_mark:Passed (after the fix): https://prover.certora.com/output/52567/75d18b94dee042a98d80ba9826a66417/?anonymousKey=b8999a782ea5486f333b616abe65aa0ce09a1767

**Licredity:** Fixed in [PR#63](https://github.com/Licredity/licredity-v1-core/pull/63/files), commit [`a15c17f`](https://github.com/Licredity/licredity-v1-core/commit/a15c17f2d871cb8cfa30814c41c43596211617fe)

**Cyfrin:** Verified, `to` verified to not be `address(0)`.
