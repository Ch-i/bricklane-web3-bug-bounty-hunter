---
affected_contracts: []
derives_from: []
id: solodit-0x52-2024-08-25-adapterfi-yield-bearing-allocator-1-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-08-25T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-08-25-AdapterFi-Yield-Bearing-Allocator.md
tags:
- firm:0x52
- report:2024-08-25-adapterfi-yield-bearing-allocator
title: '[M-03] Incorrect inequality in `YieldBearingAssetFundsAllocator#_generate_balance_txs`
  can lead to withdrawal DOS'
vuln_class: []
---

# [M-03] Incorrect inequality in `YieldBearingAssetFundsAllocator#_generate_balance_txs` can lead to withdrawal DOS

_Section severity (from Solodit section header): Medium_  
_Audit firm: 0x52_  
_Source report: [2024-08-25-AdapterFi-Yield-Bearing-Allocator.md](https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-08-25-AdapterFi-Yield-Bearing-Allocator.md)_

---

**Details**

[YieldBearingAssetFundsAllocator.vy#L273-L277](https://github.com/adapter-fi/AdapterVault/blob/a5172a63abedd4e19c9e1a17b06d579760b4aba6/contracts/YieldBearingAssetFundsAllocator.vy#L273-L277)

    if convert(shortfall, int256) > max(_adapter_states[i].max_withdraw, _adapter_states[i].max_withdraw):
        # Got it all!
        adapter_txs.append( BalanceTX({qty: convert(shortfall, int256) * -1,
                            adapter: _adapter_states[i].adapter}) )
        shortfall = 0

In the above check, shortfall is compared against max_withdraw to determine if the adapter is able to cover the shortfall. The problem is that shortfall is a positive number (higher signifies greater) while max_withdraw is a negative number (lower signifies greater). Since shortfall > 0 and max_withdraw < 0, this will always return true. In the event that `|max_withdraw| < shortfall` or `current < shortfall` the withdrawal will revert during execution, which will DOS withdrawals from the vault.

**Lines of Code**

[YieldBearingAssetFundsAllocator.vy#L273-L277](https://github.com/adapter-fi/AdapterVault/blob/a5172a63abedd4e19c9e1a17b06d579760b4aba6/contracts/YieldBearingAssetFundsAllocator.vy#L273-L277)

[YieldBearingAssetFundsAllocator.vy#L290-L299](https://github.com/adapter-fi/AdapterVault/blob/a5172a63abedd4e19c9e1a17b06d579760b4aba6/contracts/YieldBearingAssetFundsAllocator.vy#L290-L299)

**Recommendation**

abs(max_withdraw) should be used when comparing with shortfall

**Remediation**

Fix in commit [5996492](https://github.com/adapter-fi/AdapterVault/commit/5996492b8bdfbc1b544b4e12e0a7966c381cba50) as recommended.
