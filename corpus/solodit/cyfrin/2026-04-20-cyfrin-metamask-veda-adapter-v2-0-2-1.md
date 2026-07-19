---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-20-cyfrin-metamask-veda-adapter-v2-0-2-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-04-20T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-20-cyfrin-metamask-veda-adapter-v2.0.md
tags:
- firm:cyfrin
- report:2026-04-20-cyfrin-metamask-veda-adapter-v2-0
title: Eliminate single-use `encodedTransfer_` local variable
vuln_class: []
---

# Eliminate single-use `encodedTransfer_` local variable

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-20-cyfrin-metamask-veda-adapter-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-20-cyfrin-metamask-veda-adapter-v2.0.md)_

---

**Description:** In both `VedaAdapter::_executeDepositByDelegation` and `VedaAdapter::_executeWithdrawByDelegation`, the `encodedTransfer_` variable is assigned once and consumed on the immediately following line. Inlining the expression removes the extra local and avoids a trivial memory allocation:

```solidity
// src/helpers/VedaAdapter.sol
346:    bytes memory encodedTransfer_ = abi.encodeCall(IERC20.transfer, (address(this), amount_));
347:    executionCallDatas_[0] = ExecutionLib.encodeSingle(token_, 0, encodedTransfer_);

392:    bytes memory encodedTransfer_ = abi.encodeCall(IERC20.transfer, (address(this), shareAmount_));
393:    executionCallDatas_[0] = ExecutionLib.encodeSingle(boringVault, 0, encodedTransfer_);
```

**Recommended Mitigation:** Inline the `abi.encodeCall` expression directly:

```diff
- bytes memory encodedTransfer_ = abi.encodeCall(IERC20.transfer, (address(this), amount_));
- executionCallDatas_[0] = ExecutionLib.encodeSingle(token_, 0, encodedTransfer_);
+ executionCallDatas_[0] = ExecutionLib.encodeSingle(token_, 0, abi.encodeCall(IERC20.transfer, (address(this), amount_)));
```

Apply the same change to the withdraw path.

**MetaMask:** Fixed in commit [`adb6c64`](https://github.com/MetaMask/delegation-framework/pull/166/changes/adb6c64e92f75bf9dacc5528ef0da9a74b6853b7)

**Cyfrin:** Verified.

\clearpage
