---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-01-cyfrin-metamask-delegationframework2-v2-0-3-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-04-01T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-01-cyfrin-Metamask-DelegationFramework2-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-01-cyfrin-metamask-delegationframework2-v2-0
title: '`NativeTokenStreamingEnforcer` and `ERC20TokenStreamingEnforcer` gas optimizations'
vuln_class: []
---

# `NativeTokenStreamingEnforcer` and `ERC20TokenStreamingEnforcer` gas optimizations

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-01-cyfrin-Metamask-DelegationFramework2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-01-cyfrin-Metamask-DelegationFramework2-v2.0.md)_

---

**Description:**
1. Cache the amount spent to avoid multiple storage reads:
```diff
    function _validateAndConsumeAllowance(
        bytes calldata _terms,
        bytes calldata _executionCallData,
        bytes32 _delegationHash,
        address _redeemer
    )
        private
    {
        (, uint256 value_,) = _executionCallData.decodeSingle();
        (uint256 initialAmount_, uint256 maxAmount_, uint256 amountPerSecond_, uint256 startTime_) = getTermsInfo(_terms);
        require(maxAmount_ >= initialAmount_, "NativeTokenStreamingEnforcer:invalid-max-amount");
        require(startTime_ > 0, "NativeTokenStreamingEnforcer:invalid-zero-start-time");
        StreamingAllowance storage allowance_ = streamingAllowances[msg.sender][_delegationHash];
++      uint256 currentAmountSpent = allowance_.spent;
--      if (allowance_.spent == 0) {
++      if (currentAmountSpent == 0) {
            // First use of this delegation
            allowance_.initialAmount = initialAmount_;
            allowance_.maxAmount = maxAmount_;
            allowance_.amountPerSecond = amountPerSecond_;
            allowance_.startTime = startTime_;
        }
        require(value_ <= _getAvailableAmount(allowance_), "NativeTokenStreamingEnforcer:allowance-exceeded");
--      allowance_.spent += value_;
++      allowance_.spent = value_ + currentAmountSpent;
        emit IncreasedSpentMap(
            msg.sender,
            _redeemer,
            _delegationHash,
            initialAmount_,
            maxAmount_,
            amountPerSecond_,
            startTime_,
--          allowance_.spent,
++          value_ + currentAmountSpent,
            block.timestamp
        );
    }
```

2. Avoid overriding storage data when spent is 0 and data is already set
```diff
    function _validateAndConsumeAllowance(
        bytes calldata _terms,
        bytes calldata _executionCallData,
        bytes32 _delegationHash,
        address _redeemer
    )
        private
    {
        ...
        StreamingAllowance storage allowance_ = streamingAllowances[msg.sender][_delegationHash];
--      if (allowance_.spent == 0) {
++      if (allowance_.spent == 0 && allowance_.startTime == 0) {
            // First use of this delegation
            allowance_.initialAmount = initialAmount_;
            allowance_.maxAmount = maxAmount_;
            allowance_.amountPerSecond = amountPerSecond_;
            allowance_.startTime = startTime_;
        }
        ...
    }
```

3. Total spent is impossible to be greater than the amount unlocked, hence checking if the amount spent is greater than or equal to the amount unlocked is unnecessary. Just a single equal operator is enough:
```diff
    function _getAvailableAmount(StreamingAllowance memory _allowance) private view returns (uint256) {
        if (block.timestamp < _allowance.startTime) return 0;
        uint256 elapsed_ = block.timestamp - _allowance.startTime;
        uint256 unlocked_ = _allowance.initialAmount + (_allowance.amountPerSecond * elapsed_);
        if (unlocked_ > _allowance.maxAmount) {
            unlocked_ = _allowance.maxAmount;
        }
--      if (_allowance.spent >= unlocked_) return 0;
++      if (_allowance.spent == unlocked_) return 0;
        return unlocked_ - _allowance.spent;
    }
```

**Metamask:** Acknowledged.

**Cyfrin:** Acknowledged.
