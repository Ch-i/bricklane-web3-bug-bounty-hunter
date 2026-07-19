---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-18-cyfrin-ondo-finance-2-8
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-04-18T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md
tags:
- firm:cyfrin
- report:2024-04-18-cyfrin-ondo-finance
title: In `OUSGInstantManager::_mint` and `_redeem` cache `feeReceiver` and only emit
  fee event if fees are deducted
vuln_class: []
---

# In `OUSGInstantManager::_mint` and `_redeem` cache `feeReceiver` and only emit fee event if fees are deducted

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-18-cyfrin-ondo-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md)_

---

**Description:** In `OUSGInstantManager::_mint` cache `feeReceiver` and only emit fee event if fees are deducted to save 1 storage read:
```solidity
    // Transfer USDC
    if (usdcFees > 0) {
      // @audit GAS - cache `feeReceiver` and only emit fee event if
      // fees are deducted
      address feeReceiverCached = feeReceiver;

      usdc.transferFrom(msg.sender, feeReceiverCached, usdcFees);
      emit MintFeesDeducted(msg.sender, feeReceiverCached, usdcFees, usdcAmountIn);
    }
```

A similar optimization can be made in `_redeem`.

**Ondo:**
Acknowledged.
