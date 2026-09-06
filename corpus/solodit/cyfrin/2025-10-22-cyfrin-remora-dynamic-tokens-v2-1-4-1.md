---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-22-cyfrin-remora-dynamic-tokens-v2-1-4-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-10-22T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-22-cyfrin-remora-dynamic-tokens-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-22-cyfrin-remora-dynamic-tokens-v2-1
title: Consider explicitly denying `allowUser` assigning admin privileges to`ChildToken`
  contracts
vuln_class: []
---

# Consider explicitly denying `allowUser` assigning admin privileges to`ChildToken` contracts

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-22-cyfrin-remora-dynamic-tokens-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-22-cyfrin-remora-dynamic-tokens-v2.1.md)_

---

**Description:** The 1:1 invariant of a child token can be broken as follows:

Admin:
- calls `allowUser` on a child token contract
- calls `transfer` to directly send central token to the child token

This breaks the 1:1 invariant.

This is clearly something only a malicious admin would do, so this has been classified as Informational.

**Impact:** 1:1 invariant of child token is broken, bricking any further minting.

**Proof of Concept:** Add this to `CentralTokenTest.t.sol`

```solidity
    function test_cyfrin_brickMintingByAllowingChildTokenAsAdmin() public {
        address dom = getDomesticUser(0);
        centralTokenProxy.mint(address(this), uint64(4));

        allowListProxy.allowUser(address(d_childTokenProxy), true, true, true);
        centralTokenProxy.transfer(address(d_childTokenProxy), 1);


        vm.expectRevert(bytes4(keccak256("CentralBalanceInvariant()")));
        centralTokenProxy.dynamicTransfer(dom, 3);
    }
```
**Remora:** Fixed at commit [2fc2c11](https://github.com/remora-projects/remora-dynamic-tokens/commit/2fc2c119b8cec8f46ccd9bacf5cb9ead1c040484).

**Cyfrin:** Verified. `transfer()` and `transferFrom()` are overridden preventing ChildTokens from receiving CentralTokens via a direct transfer or transferFrom.
