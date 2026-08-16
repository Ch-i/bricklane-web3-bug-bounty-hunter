---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-01-cyfrin-metamask-delegationframework2-v2-0-3-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-04-01T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-01-cyfrin-Metamask-DelegationFramework2-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-01-cyfrin-metamask-delegationframework2-v2-0
title: '`ERC20PeriodTransferEnforcer` gas optimizations'
vuln_class: []
---

# `ERC20PeriodTransferEnforcer` gas optimizations

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-01-cyfrin-Metamask-DelegationFramework2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-01-cyfrin-Metamask-DelegationFramework2-v2.0.md)_

---

**Description:**
1. The current implementation of `_validateAndConsumeTransfer` performs several validations on every function call, even though some of these validations are only need to be performed once during the first execution for a given delegation hash. Since the terms of a delegation are immutable and time only increases, these checks become redundant after the first successful execution. This causes unnecessary gas consumption on subsequent calls. Consider moving the term validations and time check inside the initialization block so they're only performed once per delegation hash.
```diff
    function _validateAndConsumeTransfer(
        bytes calldata _terms,
        bytes calldata _executionCallData,
        bytes32 _delegationHash,
        address _redeemer
    )
        private
    {
        ...

        // Validate terms
--      require(startDate_ > 0, "ERC20PeriodTransferEnforcer:invalid-zero-start-date");
--      require(periodDuration_ > 0, "ERC20PeriodTransferEnforcer:invalid-zero-period-duration");
--      require(periodAmount_ > 0, "ERC20PeriodTransferEnforcer:invalid-zero-period-amount");

        require(token_ == target_, "ERC20PeriodTransferEnforcer:invalid-contract");
        require(bytes4(callData_[0:4]) == IERC20.transfer.selector, "ERC20PeriodTransferEnforcer:invalid-method");

        // Ensure the transfer period has started.
--      require(block.timestamp >= startDate_, "ERC20PeriodTransferEnforcer:transfer-not-started");

        PeriodicAllowance storage allowance_ = periodicAllowances[msg.sender][_delegationHash];

        // Initialize the allowance on first use.
        if (allowance_.startDate == 0) {
            allowance_.periodAmount = periodAmount_;
            allowance_.periodDuration = periodDuration_;
            allowance_.startDate = startDate_;
            allowance_.lastTransferPeriod = 0;
            allowance_.transferredInCurrentPeriod = 0;

++          require(startDate_ > 0, "ERC20PeriodTransferEnforcer:invalid-zero-start-date");
++          require(periodDuration_ > 0, "ERC20PeriodTransferEnforcer:invalid-zero-period-duration");
++          require(periodAmount_ > 0, "ERC20PeriodTransferEnforcer:invalid-zero-period-amount");
++          require(block.timestamp >= startDate_, "ERC20PeriodTransferEnforcer:transfer-not-started");
        }

        ...
    }
```

2. Unnecessary storage writes
```diff
    function _validateAndConsumeTransfer(
        bytes calldata _terms,
        bytes calldata _executionCallData,
        bytes32 _delegationHash,
        address _redeemer
    )
        private
    {
        ...
        PeriodicAllowance storage allowance_ = periodicAllowances[msg.sender][_delegationHash];
        // Initialize the allowance on first use.
        if (allowance_.startDate == 0) {
            allowance_.periodAmount = periodAmount_;
            allowance_.periodDuration = periodDuration_;
            allowance_.startDate = startDate_;
--          allowance_.lastTransferPeriod = 0;
--          allowance_.transferredInCurrentPeriod = 0;
        }
        ...
    }
```
These 2 variables are updated afterwards and are already initialized at 0. Hence, it makes no sense to set them to 0 upon initialization.

3. Unnecessary storage read
```diff
    function _validateAndConsumeTransfer(
        bytes calldata _terms,
        bytes calldata _executionCallData,
        bytes32 _delegationHash,
        address _redeemer
    )
        private
    {
        emit TransferredInPeriod(
            msg.sender,
            _redeemer,
            _delegationHash,
            token_,
            periodAmount_,
            periodDuration_,
--          allowance_.startDate,
++          startDate_,
            allowance_.transferredInCurrentPeriod,
            block.timestamp
        );
    }
```
No need to read the start date from storage because it is already cached

**Metamask:** Resolved in commit [d08147](https://github.com/MetaMask/delegation-framework/commit/d0814747409cf41d098e369e3f481fbb6a24e92).

**Cyfrin:** Resolved.
