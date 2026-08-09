---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-09-cyfrin-matrixdock-v2-0-0-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-04-09T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-09-cyfrin-matrixdock-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-09-cyfrin-matrixdock-v2-0
title: Cross-chain blocked recipients aren't properly handled
vuln_class: []
---

# Cross-chain blocked recipients aren't properly handled

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-09-cyfrin-matrixdock-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-09-cyfrin-matrixdock-v2.0.md)_

---

**Description:** The `MToken` contract implements a blocking mechanism to prevent certain addresses from interacting with the token. However, the cross-chain functionality doesn't properly handle blocked addresses.

There are two key issues:

1. In `MToken::msgOfCcSendToken`, the contract checks if the `receiver` is blocked on the source chain, but this check is invalid since the receiver exists on the destination chain.
```solidity
369:    function msgOfCcSendToken(
370:        address sender,
371:        address receiver,
372:        uint256 value
373:    ) public view returns (bytes memory message) {
374:        _checkBlocked(sender);
375:        _checkBlocked(receiver);//@audit-issue receiver is not on the same chain, so this check does not make sense
376:        return abi.encode(TagSendToken, abi.encode(sender, receiver, value));
377:    }
```

2. In `MToken::ccReceiveToken`, there's no check to verify if the `receiver` is blocked on the current (destination) chain before minting tokens to them.
```solidity
415:    function ccReceiveToken(bytes memory message) internal {
416:        (address sender, address receiver, uint value) = abi.decode(
417:            message,
418:            (address, address, uint)
419:        );
420:        _mint(receiver, value);//@audit-issue should check if receiver is blocked, might need to manage the funds sent to the blocked address
421:        emit CCReceiveToken(sender, receiver, value);
422:    }
```
These issues could allow blocked addresses to receive tokens via cross-chain transfers, bypassing the security controls intended by the protocol.

**Impact:** The blocking mechanism can be bypassed using cross-chain transfers. Malicious or sanctioned addresses that are blocked on one chain can still receive tokens through cross-chain transfers, undermining the security feature of the protocol.

**Proof Of Concept:**
```solidity
    // Test cross-chain sending to a blocked address
    function testCrossChainSendToken_ToBlockedAddress() public {
        // Mint some tokens to user1
        uint256 amount = 100 * 10**18;
        mintTokens(user1, amount);

        // Block user2 on the destination chain
        vm.prank(operator);
        remoteChainMToken.addToBlockedList(user2);

        // User1 tries to send tokens cross-chain to blocked user2
        vm.startPrank(user1);
        mtoken.approve(address(mockMessager), amount);

        // When sending to a blocked address, the send may succeed but the tokens should never reach the destination
        mockMessager.sendTokenToChain{value: 0.01 ether}(
            CHAIN_SELECTOR_2,
            address(remoteChainMToken),
            user2,
            amount,
            ""
        );
        vm.stopPrank();

        // Check that user1's tokens are gone (burned in the sending process)
        assertEq(mtoken.balanceOf(user1), 0, "Tokens should be burned on source chain");

        // The blocked user should NOT receive any tokens
        // assertEq(remoteChainMToken.balanceOf(user2), 0, "Blocked user should not receive tokens");
    }
```

**Recommended Mitigation:**
1. Remove the receiver check in `msgOfCcSendToken` as it's not relevant to the source chain:

```diff
function msgOfCcSendToken(
    address sender,
    address receiver,
    uint256 value
) public view returns (bytes memory message) {
    _checkBlocked(sender);
-   _checkBlocked(receiver);
    return abi.encode(TagSendToken, abi.encode(sender, receiver, value));
}
```

2. Add a blocked address check in `ccReceiveToken` and implement a mechanism to handle tokens sent to blocked addresses:

```diff
function ccReceiveToken(bytes memory message) internal {
    (address sender, address receiver, uint value) = abi.decode(
        message,
        (address, address, uint)
    );
+   if (isBlocked[receiver]) {
+       // Option 1: Send to a recovery address
+       _mint(operator, value);
+       emit CCReceiveBlockedAddress(sender, receiver, value);
+   } else {
        _mint(receiver, value);
+   }
    emit CCReceiveToken(sender, receiver, value);
}
```

**Matrixdock:** Acknowledged.


\clearpage
