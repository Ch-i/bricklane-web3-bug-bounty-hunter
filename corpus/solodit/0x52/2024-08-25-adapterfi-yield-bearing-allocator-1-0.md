---
affected_contracts: []
derives_from: []
id: solodit-0x52-2024-08-25-adapterfi-yield-bearing-allocator-1-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-08-25T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-08-25-AdapterFi-Yield-Bearing-Allocator.md
tags:
- firm:0x52
- report:2024-08-25-adapterfi-yield-bearing-allocator
title: '[M-01] Withdraw limits are not properly considered during balancing transactions
  and can lead to vault DOS'
vuln_class: []
---

# [M-01] Withdraw limits are not properly considered during balancing transactions and can lead to vault DOS

_Section severity (from Solodit section header): Medium_  
_Audit firm: 0x52_  
_Source report: [2024-08-25-AdapterFi-Yield-Bearing-Allocator.md](https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-08-25-AdapterFi-Yield-Bearing-Allocator.md)_

---

**Details**

When withdrawing from an adapter, current balance and max withdraw must be considered. If either is exceeded then the rebalance transaction will revert during execution and will revert the entire transaction causing a vault DOS.

[YieldBearingAssetFundsAllocator.vy#L244-L254](https://github.com/adapter-fi/AdapterVault/blob/a5172a63abedd4e19c9e1a17b06d579760b4aba6/contracts/YieldBearingAssetFundsAllocator.vy#L244-L254)

    if shortfall > 0 and min_delta_withdraw_pos != MAX_ADAPTERS:
        if _adapter_states[min_delta_withdraw_pos].current > shortfall:
            # Got it all!
            adapter_txs.append( BalanceTX({qty: convert(shortfall, int256) * -1,
                                            adapter: _adapter_states[min_delta_withdraw_pos].adapter}) )
            shortfall = 0
        else:
            # Got some...
            adapter_txs.append( BalanceTX({qty: convert(_adapter_states[min_delta_withdraw_pos].current, int256) * -1,
                                            adapter: _adapter_states[min_delta_withdraw_pos].adapter}) )
            shortfall -= _adapter_states[min_delta_withdraw_pos].current

Above we see that only the current balance of the adapter is considered. This leads and edge case in which `current balance > shortfall > max withdraw`. Although the adapter has enough funds to cover the withdrawal, the withdrawal will revert during execution due to the amount being higher than the max withdraw amount.

[YieldBearingAssetFundsAllocator.vy#L290-L299](https://github.com/adapter-fi/AdapterVault/blob/a5172a63abedd4e19c9e1a17b06d579760b4aba6/contracts/YieldBearingAssetFundsAllocator.vy#L290-L299)

    if convert(shortfall, int256) > max(_adapter_states[i].max_withdraw, _adapter_states[i].max_withdraw):
        # Got it all!
        adapter_txs.append( BalanceTX({qty: convert(shortfall, int256) * -1,
                            adapter: _adapter_states[i].adapter}) )
        shortfall = 0
    else:
        # Got some...
        adapter_txs.append( BalanceTX({qty: convert(_adapter_states[i].current, int256) * -1,
                            adapter: _adapter_states[i].adapter}) )
        shortfall -= _adapter_states[i].current

Here we have another similar situation but in reverse. The max withdraw is checked but then current balance or shortfall is withdrawn. This leads to the following two edge cases. The first is `max withdraw > shortfall > current balance` which will result in failure to cover the shortfall during execution. The other is `shortfall > current > max withdraw`. In this case it will attempt to withdraw the current balance which is higher than the max withdraw causing it to revert.

**Lines of Code**

[YieldBearingAssetFundsAllocator.vy#L245-L254](https://github.com/adapter-fi/AdapterVault/blob/a5172a63abedd4e19c9e1a17b06d579760b4aba6/contracts/YieldBearingAssetFundsAllocator.vy#L245-L254)

[YieldBearingAssetFundsAllocator.vy#L268-L282](https://github.com/adapter-fi/AdapterVault/blob/a5172a63abedd4e19c9e1a17b06d579760b4aba6/contracts/YieldBearingAssetFundsAllocator.vy#L268-L282)

[YieldBearingAssetFundsAllocator.vy#L285-L299](https://github.com/adapter-fi/AdapterVault/blob/a5172a63abedd4e19c9e1a17b06d579760b4aba6/contracts/YieldBearingAssetFundsAllocator.vy#L285-L299)

**Recommendation**

Whenever checking these bounds first construct a variable defined as:

    min(_adapter_states.max_withdraw * -1, _adapter_states.current)

Whenever checking limits and formulating withdrawal amounts, use this variable to account for both current balance and max withdraw at the same time.

**Remediation**

Fix in commit [5996492](https://github.com/adapter-fi/AdapterVault/commit/5996492b8bdfbc1b544b4e12e0a7966c381cba50) as recommended.
