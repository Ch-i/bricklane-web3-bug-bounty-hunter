---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-quill-finance-report-0-5
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-quill-finance-report
title: '[M-06] Risky Footguns from Bold'
vuln_class: []
---

# [M-06] Risky Footguns from Bold

_Section severity (from Solodit section header): Medium_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Quill_Finance_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md)_

---

**Impact**
These 3 lines can be VERY dangerous

https://github.com/GalloDaSballo/quill-review/blob/8d6e4c8ed0759cea1ff0376db9fd55db864cd7e8/contracts/src/Zappers/Modules/FlashLoans/BalancerFlashLoan.sol#L46-L52

```solidity
        // This will be used by the callback below no
        receiver = IFlashLoanReceiver(msg.sender);

        vault.flashLoan(this, tokens, amounts, userData);

        // Reset receiver
        receiver = IFlashLoanReceiver(address(0));
```

The reason why this code is safe for BOLD is becasue `vault` has a Reentrancy guard

In lack of that guard many projects can get exploited

**Theoretical Proof Of Code**

https://gist.github.com/GalloDaSballo/a4dd8c2b77a64d602983152d621f55c3

**Theoretical Mitigation**

- Validate AAVE initiator
- Consume the receiver

```solidity
    function receiveFlashLoan(
        IERC20[] calldata tokens,
        uint256[] calldata amounts,
        uint256[] calldata feeAmounts,
        bytes calldata userData
    ) external override {
        require(msg.sender == address(vault), "Caller is not Vault");
        require(address(receiver) != address(0), "Flash loan not properly initiated");

        // NOTE: Validate initiator (if available) (e.g. AAVE)
        // NOTE: Why not consume receiver?
        IFlashLoanReceiver public cachedReceiver = receiver;
        receiver = IFlashLoanReceiver(address(0));
```
