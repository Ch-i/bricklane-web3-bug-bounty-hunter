---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-balancer-report-2-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Balancer_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-balancer-report
title: '[I-01] Nitpick: `SAFE` and `BALANCER_MULTISIG` are the same value and are
  used inconsistently'
vuln_class: []
---

# [I-01] Nitpick: `SAFE` and `BALANCER_MULTISIG` are the same value and are used inconsistently

_Section severity (from Solodit section header): Informational_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Balancer_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Balancer_Report.md)_

---

**Impact**

The casting of `address(SAFE))` are unnecessary if you use `BALANCER_MULTISIG`

https://github.com/onchainification/aura_locker_v2/blob/07294ae3638909ecd768a6a0f831fa513abe91a0/src/AuraLockerModule.sol#L20-L21

```solidity
    address public constant BALANCER_MULTISIG = 0x10A19e7eE7d7F8a52822f6817de8ea18204F2e4f;
    IGnosisSafe public constant SAFE = IGnosisSafe(payable(BALANCER_MULTISIG));
```

Which is what's done in `onlyGovernance`

https://github.com/onchainification/aura_locker_v2/blob/07294ae3638909ecd768a6a0f831fa513abe91a0/src/AuraLockerModule.sol#L67C1-L71C6

```solidity
    /// @notice Enforce that the function is called by governance only
    modifier onlyGovernance() {
        if (msg.sender != BALANCER_MULTISIG) revert NotGovernance(msg.sender);
        _;
    }
```

**Mitigation**

You could alternatively change `onlyGovernance` to use `address(SAFE)` and make the code consistent

This has no impact on the bytecode so it's not a big deal
