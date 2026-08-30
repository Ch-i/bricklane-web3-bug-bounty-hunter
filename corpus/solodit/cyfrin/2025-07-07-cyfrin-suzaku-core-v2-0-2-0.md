---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-2-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-07-07T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-07-cyfrin-suzaku-core-v2-0
title: Missing zero-address validation for burner address during initialization can
  break slashing
vuln_class: []
---

# Missing zero-address validation for burner address during initialization can break slashing

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-07-cyfrin-suzaku-core-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md)_

---

**Description:** The VaultTokenized contract's initialization procedure fails to validate that the burner parameter is a non-zero address. However, the `onSlash` function uses SafeERC20's `safeTransfer` to send tokens to this address, which will revert for most ERC20 implementations if the recipient is address(0).

```solidity
// In _initialize:
vs.burner = params.burner; // No validation that params.burner != address(0)

// In onSlash:
if (slashedAmount > 0) {
    IERC20(vs.collateral).safeTransfer(vs.burner, slashedAmount); // Will revert if vs.burner is address(0)
}
```
While other critical parameters like collateral are validated against the zero address, the burner parameter lacks this check despite its importance in the slashing flow.

**Impact:** Setting burner to `address(0)` would break a core security function (slashing)

**Recommended Mitigation:** Consider adding a zero-address validation for the burner parameter during initialization.

**Suzaku:**
Fixed in commit [4683ab8](https://github.com/suzaku-network/suzaku-core/pull/155/commits/4683ab82c40103fd6af5a7d2447e5be211e93f20).

**Cyfrin:** Verified.
