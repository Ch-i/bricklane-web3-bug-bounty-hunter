---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-01-cyfrin-metamask-delegationframework2-v2-0-3-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-04-01T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-01-cyfrin-Metamask-DelegationFramework2-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-01-cyfrin-metamask-delegationframework2-v2-0
title: Unnecessary execution mode support in `DelegationMetaSwapAdapter`
vuln_class: []
---

# Unnecessary execution mode support in `DelegationMetaSwapAdapter`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-01-cyfrin-Metamask-DelegationFramework2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-01-cyfrin-Metamask-DelegationFramework2-v2.0.md)_

---

**Description:** The `executeFromExecutor` function in the `DelegationMetaSwapAdapter` supports multiple execution modes (batch/single) and execution types (default/try). However, in practice, the adapter's main function swapByDelegation only ever uses the encodeSimpleSingle mode with default execution type.

This implementation includes complex conditional logic that handles multiple code paths that are never utilized in the current application:


```solidity
    function swapByDelegation(bytes calldata _apiData, Delegation[] memory _delegations) external {
        ...
        ModeCode[] memory encodedModes_ = new ModeCode[](2);
        encodedModes_[0] = ModeLib.encodeSimpleSingle();
        encodedModes_[1] = ModeLib.encodeSimpleSingle();
        ...
    }

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

**Recommendation**
Consider restricting the `executeFromExecutor` function to only support the execution modes that are actually used in the application:

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

    // Only support single call type with default execution
    if (callType_ != CALLTYPE_SINGLE) {
        revert UnsupportedCallType(callType_);
    }

    if (execType_ != EXECTYPE_DEFAULT) {
        revert UnsupportedExecType(execType_);
    }

    // Process single execution directly without additional checks
    (address target_, uint256 value_, bytes calldata callData_) = _executionCalldata.decodeSingle();
    returnData_ = new bytes[](1);
    returnData_[0] = _execute(target_, value_, callData_);

    return returnData_;
}
```

**Metamask:** Resolved in commit [afb243c](https://github.com/MetaMask/delegation-framework/commit/afb243cdff4960c51170f58e0058912e7dec392a).

**Cyfrin:** Resolved.

\clearpage
