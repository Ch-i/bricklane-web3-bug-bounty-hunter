---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-01-cyfrin-sorella-l2-angstrom-v2-1-3-4
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-10-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-01-cyfrin-sorella-l2-angstrom-v2-1
title: Consider burning `ERC-6909` claim tokens within `AngstromL2::withdrawProtocolRevenue`
  and transferring the underlying asset instead
vuln_class: []
---

# Consider burning `ERC-6909` claim tokens within `AngstromL2::withdrawProtocolRevenue` and transferring the underlying asset instead

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md)_

---

**Description:** `AngstromL2::withdrawProtocolRevenue` currently transfers `ERC-6909` balance to the recipient; however, this address may lack the capability to easily burn the claim token. Instead, it may be preferable to perform this step within a Uniswap V4 `PoolManager` callback prior to transferring the underlying asset and then ending execution.

```solidity
UNI_V4.transfer(to, assetId, amount);
```

**Sorella Labs:** Fixed in commit [ffb9fb2](https://github.com/SorellaLabs/l2-angstrom/commit/ffb9fb20e5b0afbf6996ef9528ef10acd8c94f91#diff-0e68badc81333f3e60fad8069459c6e57e1ac84f433fb40f23cda776b9f9442b).

**Cyfrin:** Verified. The underlying currency is now transferred directly.
