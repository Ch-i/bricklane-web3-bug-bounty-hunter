---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-13-cyfrin-zaros-3-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-07-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md
tags:
- firm:cyfrin
- report:2024-07-13-cyfrin-zaros
title: Unused variables
vuln_class: []
---

# Unused variables

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-13-cyfrin.zaros.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md)_

---

**Description:** Some errors and constants aren't used in the codebase.

```solidity
File: Errors.sol
11:     error InvalidParameter(string parameter, string reason);
38:     error OnlyForwarder(address sender, address forwarder);
79:     error InvalidLiquidationReward(uint128 liquidationFeeUsdX18);

File: Constants.sol
10:     uint32 internal constant MAX_MIN_DELEGATE_TIME = 30 days;
```

**Zaros:** Fixed in commit [37071ed](https://github.com/zaros-labs/zaros-core/commit/37071ed2c6845121e2eda4143ad233d20a1d7e6f).

**Cyfrin:** Verified.
