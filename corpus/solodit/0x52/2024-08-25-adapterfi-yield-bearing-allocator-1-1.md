---
affected_contracts: []
derives_from: []
id: solodit-0x52-2024-08-25-adapterfi-yield-bearing-allocator-1-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-08-25T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-08-25-AdapterFi-Yield-Bearing-Allocator.md
tags:
- firm:0x52
- report:2024-08-25-adapterfi-yield-bearing-allocator
title: '[M-02] `YieldBearingAssetFundsAllocator#_allocate_balance_adapter_tx` fails
  to properly apply `ADAPTER_BREAKS_LOSS_POINT`'
vuln_class: []
---

# [M-02] `YieldBearingAssetFundsAllocator#_allocate_balance_adapter_tx` fails to properly apply `ADAPTER_BREAKS_LOSS_POINT`

_Section severity (from Solodit section header): Medium_  
_Audit firm: 0x52_  
_Source report: [2024-08-25-AdapterFi-Yield-Bearing-Allocator.md](https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-08-25-AdapterFi-Yield-Bearing-Allocator.md)_

---

**Details**

[YieldBearingAssetFundsAllocator.vy#L407-L414](https://github.com/adapter-fi/AdapterVault/blob/a5172a63abedd4e19c9e1a17b06d579760b4aba6/contracts/YieldBearingAssetFundsAllocator.vy#L407-L414)

    should_we_block_adapter : bool = False
    if _balance_adapter.current < _balance_adapter.last_value:
        # There's an unexpected loss of value. Let's try to empty this adapter and stop
        # further allocations to it by setting the ratio to 0 going forward.
        # This will not necessarily result in any "leftovers" unless withdrawing the full
        # balance of the adapter is limited by max_withdraw limits below.
        _balance_adapter.ratio = 0
        should_we_block_adapter = True

When allocating funds to adapters, the above code checks if the current value is lower than the previous value. If there is even a single wei below it will block the adapter. This is especially problematic for adapters that are based on the market prices (such as the pendle adapter) as they will be frequently disabled.

`ADAPTER_BREAKS_LOSS_POINT` was present in previous version but is notably absent in this one.

**Lines of Code**

[YieldBearingAssetFundsAllocator.vy#L403-L434](https://github.com/adapter-fi/AdapterVault/blob/a5172a63abedd4e19c9e1a17b06d579760b4aba6/contracts/YieldBearingAssetFundsAllocator.vy#L403-L434)

**Recommendation**

Reintroduce `ADAPTER_BREAKS_LOSS_POINT` and only block the adapter if losses exceed that margin.

**Remediation**

Fix in commit [b344fd3](https://github.com/adapter-fi/AdapterVault/commit/b344fd3c129afdd42dcdbc7026b1a0c39c6ac29c) as recommended.
