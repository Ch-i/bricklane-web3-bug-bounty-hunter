---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-01-cyfrin-metamask-delegationframework2-v2-0-1-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-04-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-01-cyfrin-Metamask-DelegationFramework2-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-01-cyfrin-metamask-delegationframework2-v2-0
title: Bugged `erc7579-implementation` commit imported
vuln_class: []
---

# Bugged `erc7579-implementation` commit imported

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-01-cyfrin-Metamask-DelegationFramework2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-01-cyfrin-Metamask-DelegationFramework2-v2.0.md)_

---

**Description:** Currently, the codebase imports the `erc7579-implementation` external repository at commit `42aa538397138e0858bae09d1bd1a1921aa24b8c `to use the `ExecutionHelper`. This import is used inside the `DelegationMetaSwapAdapter` to implement the `executeFromExecutor` method:
```solidity
    function executeFromExecutor(
        ModeCode _mode,
        bytes calldata _executionCalldata
    )
        external
        payable
        onlyDelegationManager
        returns (bytes[] memory returnData_)
    {
        (CallType callType_, ExecType execType_,,) = _mode.decode();

        // Check if calltype is batch or single
        if (callType_ == CALLTYPE_BATCH) {
            // Destructure executionCallData according to batched exec
            Execution[] calldata executions_ = _executionCalldata.decodeBatch();
            // check if execType is revert or try
            if (execType_ == EXECTYPE_DEFAULT) returnData_ = _execute(executions_);
            else if (execType_ == EXECTYPE_TRY) returnData_ = _tryExecute(executions_);
            else revert UnsupportedExecType(execType_);
        } else if (callType_ == CALLTYPE_SINGLE) {
            // Destructure executionCallData according to single exec
            (address target_, uint256 value_, bytes calldata callData_) = _executionCalldata.decodeSingle();
            returnData_ = new bytes[](1);
            bool success_;
            // check if execType is revert or try
            if (execType_ == EXECTYPE_DEFAULT) {
                returnData_[0] = _execute(target_, value_, callData_);
            } else if (execType_ == EXECTYPE_TRY) {
                (success_, returnData_[0]) = _tryExecute(target_, value_, callData_);
                if (!success_) emit TryExecuteUnsuccessful(0, returnData_[0]);
            } else {
                revert UnsupportedExecType(execType_);
            }
        } else {
            revert UnsupportedCallType(callType_);
        }
    }
```
When the `execType` is set to be `EXECTYPE_TRY`, the interal `_tryExecute` method is executed:
```solidity
    function _tryExecute(
        address target,
        uint256 value,
        bytes calldata callData
    )
        internal
        virtual
        returns (bool success, bytes memory result)
    {
        /// @solidity memory-safe-assembly
        assembly {
            result := mload(0x40)
            calldatacopy(result, callData.offset, callData.length)
@>          success := iszero(call(gas(), target, value, result, callData.length, codesize(), 0x00))
            mstore(result, returndatasize()) // Store the length.
            let o := add(result, 0x20)
            returndatacopy(o, 0x00, returndatasize()) // Copy the returndata.
            mstore(0x40, add(o, returndatasize())) // Allocate the memory.
        }
    }
```
This function executes a low level call and assigns the success the result of the call applying an is zero operator. This implementation is wrong because the result of a low level call already returns 1 on success and 0 on error. So applying an is zero operator will flip the result and be erroneus.
The result of this will be that when executing a transaction in try mode, successful executions will emit the `TryExecuteUnsuccessful` and failing executions will not. This can confuse the user if these events are used by the UI.

**Impact:** Incorrect event emission

**Recommended Mitigation:** Consider updating the commit version to the latest one, [it does not have this bug anymore](https://github.com/erc7579/erc7579-implementation/blob/main/src/core/ExecutionHelper.sol#L81)


**MetaMask:**
Resolved in commit [73e719](https://github.com/MetaMask/delegation-framework/commit/73e719dd25fe990d614f00203f089f4fd8b4761c).

**Cyfrin:** Resolved.
