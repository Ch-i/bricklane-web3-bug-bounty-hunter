---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-01-cyfrin-metamask-delegationframework2-v2-0-1-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-04-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-01-cyfrin-Metamask-DelegationFramework2-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-01-cyfrin-metamask-delegationframework2-v2-0
title: Wrong event data field in `ERC20PeriodTransferEnforcer`
vuln_class: []
---

# Wrong event data field in `ERC20PeriodTransferEnforcer`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-01-cyfrin-Metamask-DelegationFramework2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-01-cyfrin-Metamask-DelegationFramework2-v2.0.md)_

---

**Description:** In the `ERC20PeriodTransferEnforcer` it emits the following event when this caveat is used:
```solidity
    /**
     * @notice Emitted when a transfer is made, updating the transferred amount in the active period.
     * @param sender The address initiating the transfer.
@>   * @param recipient The address that receives the tokens.
     * @param delegationHash The hash identifying the delegation.
     * @param token The ERC20 token contract address.
     * @param periodAmount The maximum tokens transferable per period.
     * @param periodDuration The duration of each period (in seconds).
     * @param startDate The timestamp when the first period begins.
     * @param transferredInCurrentPeriod The total tokens transferred in the current period after this transfer.
     * @param transferTimestamp The block timestamp at which the transfer was executed.
     */
    event TransferredInPeriod(
        address indexed sender,
@>      address indexed recipient,
        bytes32 indexed delegationHash,
        address token,
        uint256 periodAmount,
        uint256 periodDuration,
        uint256 startDate,
        uint256 transferredInCurrentPeriod,
        uint256 transferTimestamp
    );
```
As we can see, the second field is the token recipient. However, in other token related caveats such as `ERC20StreamingEnforcer` and `NativeTokenStreamingEnforcer` the second field in the emitted event data is the `redeemer`, the address that redeems the delegation.

It makes sense that this should be the intended behavior because the data passed to the event is indeed the `redeemer`:
```solidity
    function _validateAndConsumeTransfer(
        bytes calldata _terms,
        bytes calldata _executionCallData,
        bytes32 _delegationHash,
        address _redeemer
    )
        private
    {
        ...
        emit TransferredInPeriod(
            msg.sender,
@>          _redeemer,
            _delegationHash,
            token_,
            periodAmount_,
            periodDuration_,
            allowance_.startDate,
            allowance_.transferredInCurrentPeriod,
            block.timestamp
        );
    }
```

**Impact:** The event field is misleading.

**Recommended Mitigation:**
```diff
    event TransferredInPeriod(
        address indexed sender,
--      address indexed recipient,
++      address indexed redeemer,
        bytes32 indexed delegationHash,
        address token,
        uint256 periodAmount,
        uint256 periodDuration,
        uint256 startDate,
        uint256 transferredInCurrentPeriod,
        uint256 transferTimestamp
    );
```

**MetaMask:**
Resolved in commit [15e0860](https://github.com/MetaMask/delegation-framework/commit/15e0860e45563ac4891a3b4484acbd6f66d3ab24).

**Cyfrin:** Resolved.

\clearpage
