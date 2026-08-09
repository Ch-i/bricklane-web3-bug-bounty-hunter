---
affected_contracts: []
derives_from: []
id: solodit-0x52-2024-08-25-adapterfi-yield-bearing-allocator-1-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-08-25T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-08-25-AdapterFi-Yield-Bearing-Allocator.md
tags:
- firm:0x52
- report:2024-08-25-adapterfi-yield-bearing-allocator
title: '[M-04] Blocked adapters will cause full rebalances to be DOS''d'
vuln_class: []
---

# [M-04] Blocked adapters will cause full rebalances to be DOS'd

_Section severity (from Solodit section header): Medium_  
_Audit firm: 0x52_  
_Source report: [2024-08-25-AdapterFi-Yield-Bearing-Allocator.md](https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-08-25-AdapterFi-Yield-Bearing-Allocator.md)_

---

**Details**

[YieldBearingAssetFundsAllocator.vy#L117-L136](https://github.com/adapter-fi/AdapterVault/blob/a5172a63abedd4e19c9e1a17b06d579760b4aba6/contracts/YieldBearingAssetFundsAllocator.vy#L117-L136)

    for i in range(MAX_ADAPTERS):
        rtx : BalanceAdapter = _blocked_adapters[i]
        if rtx.adapter == empty(address): break
        assert tx_pos < MAX_ADAPTERS, "Too many transactions #10!"
        result_txs[tx_pos] = BalanceTX({qty: rtx.delta, adapter: rtx.adapter}) <- @audit blocked adapter tx #1
        result_blocked[tx_blocked] = rtx.adapter
        tx_pos += 1
        tx_blocked += 1

    for i in range(MAX_ADAPTERS):
        rtx : BalanceAdapter = _adapter_states[i]
        if rtx.adapter == empty(address): break
        assert tx_pos < MAX_ADAPTERS, "Too many transactions #20!"

        # Deposits are set aside as withdraws must complete first.
        if rtx.delta > 0 and rtx.delta >= convert(_min_proposer_payout, int256) and not _withdraw_only:
            deposits_last.append(BalanceTX({qty: rtx.delta, adapter: rtx.adapter}))
        elif rtx.delta < 0:
            result_txs[tx_pos] = BalanceTX({qty: rtx.delta, adapter: rtx.adapter}) <- @audit blocked adapter tx repeat
            tx_pos += 1

When adapters lose value they are blocked and the contract attempts to withdraw all funds. In the code above we see that for a blocked adapter one `result_tx` is added during the loop through blocked adapters but then when cycling through `adapter_states` in the next block, a second `result_tx` is added for the same adapter.

When these txs are processed, the rebalance will inevitably revert leading to a DOS of the vault.

**Lines of Code**

[YieldBearingAssetFundsAllocator.vy#L108-L144](https://github.com/adapter-fi/AdapterVault/blob/a5172a63abedd4e19c9e1a17b06d579760b4aba6/contracts/YieldBearingAssetFundsAllocator.vy#L108-L144)

**Recommendation**

Adapters that are present in blocked_adapters should be skipped during the `_adapter_states` loop.

**Remediation**

Fix in commit [165cbe3](https://github.com/adapter-fi/AdapterVault/commit/165cbe34d11da444ae468693ae1d20ce9bf5c53c) as recommended.
