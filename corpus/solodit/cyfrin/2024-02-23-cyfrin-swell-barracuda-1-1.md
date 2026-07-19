---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-02-23-cyfrin-swell-barracuda-1-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-02-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md
tags:
- firm:cyfrin
- report:2024-02-23-cyfrin-swell-barracuda
title: '`swEXIT::setWithdrawRequestMaximum` and `setWithdrawRequestMinimum` lacking
  validation can lead to a state where `withdrawRequestMinimum > withdrawRequestMaximum`'
vuln_class: []
---

# `swEXIT::setWithdrawRequestMaximum` and `setWithdrawRequestMinimum` lacking validation can lead to a state where `withdrawRequestMinimum > withdrawRequestMaximum`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-02-23-cyfrin-swell-barracuda.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md)_

---

**Description:** Invariant `withdrawRequestMinimum <= withdrawRequestMaximum` must always hold, however this is not checked when new min/max withdraw values are set. Hence it is possible to enter a non-sensical state where `withdrawRequestMinimum > withdrawRequestMaximum`.

**Recommended mitigation:**
```diff
  function setWithdrawRequestMaximum(
    uint256 _withdrawRequestMaximum
  ) external override checkRole(SwellLib.PLATFORM_ADMIN) {
+   require(withdrawRequestMinimum <= _withdrawRequestMaximum);

    emit WithdrawalRequestMaximumUpdated(
      withdrawRequestMaximum,
      _withdrawRequestMaximum
    );
    withdrawRequestMaximum = _withdrawRequestMaximum;
  }

  function setWithdrawRequestMinimum(
    uint256 _withdrawRequestMinimum
  ) external override checkRole(SwellLib.PLATFORM_ADMIN) {
+   require(_withdrawRequestMinimum <= withdrawRequestMaximum);

    emit WithdrawalRequestMinimumUpdated(
      withdrawRequestMinimum,
      _withdrawRequestMinimum
    );
    withdrawRequestMinimum = _withdrawRequestMinimum;
  }
```

**Swell:** Fixed in commit [a9dfe5c](https://github.com/SwellNetwork/v3-contracts-lst/commit/a9dfe5cef35404e4e957e8001d571b1cf43feb0a).

**Cyfrin:**
Verified.
