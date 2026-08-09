---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-kleidi-report-0-8
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Kleidi_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-kleidi-report
title: '[L-09] `Timelock` prevents multiple replays, but is subject to cross operation
  reentrancy'
vuln_class: []
---

# [L-09] `Timelock` prevents multiple replays, but is subject to cross operation reentrancy

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Kleidi_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Kleidi_Report.md)_

---

**Impact**

The code for `execute` is as follows:

https://github.com/solidity-labs-io/kleidi/blob/a5f6eb7e9eb5870f2f45b4f4b93e1b4da5f5cce1/src/Timelock.sol#L595-L608

```solidity
        bytes32 id = hashOperation(target, value, payload, salt);

        /// first reentrancy check, impossible to reenter and execute the same
        /// proposal twice
        require(_liveProposals.remove(id), "Timelock: proposal does not exist");
        require(isOperationReady(id), "Timelock: operation is not ready");

        _execute(target, value, payload);
        emit CallExecuted(id, 0, target, value, payload);

        /// second reentrancy check, second check that operation is ready,
        /// operation will be not ready if already executed as timestamp will
        /// be set to 1
        _afterCall(id);
```

Before executing it will remove the `id` from liveProposals, making a double execution of the function impossible

There's a redundant check in `_afterCall(id);` that also performs a check against replay

However, the function doesn't protect against performing reentrancy between multiple operations

Meaning that mid execution of an operation, another operation could be performed

This typically can only happen when the Timelock interacts with untrusted, malicious contracts, so barring an uninteded use this shouldn't cause any major damage

**Mitigation**

Consider adding a reentrancyGuard or simply document this risk to end users to ensure they do not re-enter mid execution
