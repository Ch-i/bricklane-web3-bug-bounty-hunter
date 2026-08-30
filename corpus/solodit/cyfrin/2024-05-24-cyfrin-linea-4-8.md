---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-24-cyfrin-linea-4-8
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-05-24T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-24-cyfrin-linea.md
tags:
- firm:cyfrin
- report:2024-05-24-cyfrin-linea
title: Save 1 storage read in `L2MessageServiceV1::setMinimumFee` by emitting `MinimumFeeChanged`
  event using `_feeInWei` parameter
vuln_class: []
---

# Save 1 storage read in `L2MessageServiceV1::setMinimumFee` by emitting `MinimumFeeChanged` event using `_feeInWei` parameter

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-24-cyfrin-linea.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-24-cyfrin-linea.md)_

---

**Description:** Save 1 storage read in `L2MessageServiceV1::setMinimumFee` by emitting the `MinimumFeeChanged` event using the `_feeInWei` parameter eg:
```solidity
  function setMinimumFee(uint256 _feeInWei) external onlyRole(MINIMUM_FEE_SETTER_ROLE) {
    uint256 previousMinimumFee = minimumFeeInWei;
    minimumFeeInWei = _feeInWei;

    emit MinimumFeeChanged(previousMinimumFee, _feeInWei, msg.sender);
  }
```

**Linea:**
Acknowledged; will be part of a future release.
