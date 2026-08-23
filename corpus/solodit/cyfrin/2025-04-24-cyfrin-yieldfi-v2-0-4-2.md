---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-yieldfi-v2-0-4-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-04-24T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-24-cyfrin-yieldfi-v2-0
title: Unnecessary external call in `YToken::_decimalsOffset` and `YTokenL2::_decimalsOffset`
vuln_class: []
---

# Unnecessary external call in `YToken::_decimalsOffset` and `YTokenL2::_decimalsOffset`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-yieldfi-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md)_

---

**Description:** In [`YToken::_decimalsOffset`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/tokens/YToken.sol#L314-L316) and [`YTokenL2::_decimalsOffset`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/tokens/YTokenL2.sol#L314-L316) the decimals of the underlying token is queried:
```solidity
function _decimalsOffset() internal view virtual override returns (uint8) {
    return 18 - IERC20Metadata(asset()).decimals();
}
```
This value is however already stored in the OpenZeppelin base contract `ERC4626Upgradeable` and can be used instead of an external call.

**YieldFi:** Acknowledged.
