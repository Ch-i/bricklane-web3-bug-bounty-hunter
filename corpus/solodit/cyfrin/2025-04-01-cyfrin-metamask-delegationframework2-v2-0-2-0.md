---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-01-cyfrin-metamask-delegationframework2-v2-0-2-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-04-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-01-cyfrin-Metamask-DelegationFramework2-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-01-cyfrin-metamask-delegationframework2-v2-0
title: First transaction on `SpecificActionERC20TransferBatchEnforcer` does not support
  sending native value
vuln_class: []
---

# First transaction on `SpecificActionERC20TransferBatchEnforcer` does not support sending native value

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-01-cyfrin-Metamask-DelegationFramework2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-01-cyfrin-Metamask-DelegationFramework2-v2.0.md)_

---

**Description:** The `SpecificActionERC20TransferBatchEnforcer` is an enforcer to execute an arbitrary transaction first that is constrained by the delegator and afterwards an ERC20 transfer. Both executions are constrained to not support sending value:
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
        onlyBatchCallTypeMode(_mode)
        onlyDefaultExecutionMode(_mode)
    {
        ...

        // Validate first transaction
        if (
            executions_[0].target != terms_.firstTarget || executions_[0].value != 0
                || keccak256(executions_[0].callData) != keccak256(terms_.firstCalldata)
        ) {
            revert("SpecificActionERC20TransferBatchEnforcer:invalid-first-transaction");
        }

        // Validate second transaction
        if (
            executions_[1].target != terms_.tokenAddress || executions_[1].value != 0 || executions_[1].callData.length != 68
                || bytes4(executions_[1].callData[0:4]) != IERC20.transfer.selector
                || address(uint160(uint256(bytes32(executions_[1].callData[4:36])))) != terms_.recipient
                || uint256(bytes32(executions_[1].callData[36:68])) != terms_.amount
        ) {
            revert("SpecificActionERC20TransferBatchEnforcer:invalid-second-transaction");
        }

        ...
    }
```
This check makes sense for the ERC20 transfer execution. However, for the first transaction may be too limited for the delegator that may want to include value along with the execution.

**Recommended Mitigation:** Consider removing the value check for the first transaction to enable the delegator to have more freedom when constraining the first execution. Note that the delegator can always constrain the value field with other enforcers.
```diff
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
        onlyBatchCallTypeMode(_mode)
        onlyDefaultExecutionMode(_mode)
    {
        ...

        // Validate first transaction
        if (
--          executions_[0].target != terms_.firstTarget || executions_[0].value != 0
++          executions_[0].target != terms_.firstTarget
                || keccak256(executions_[0].callData) != keccak256(terms_.firstCalldata)
        ) {
            revert("SpecificActionERC20TransferBatchEnforcer:invalid-first-transaction");
        }
        ...
    }
```

**Metamask:** Acknowledged. We need this for a specific use case where native token (ETH) is not involved.

**Cyfrin:** Acknowledged.

\clearpage
