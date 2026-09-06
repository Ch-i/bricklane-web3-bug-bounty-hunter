---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-15-cyfrin-earnm-dropbox-v2-0-4-7
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-08-15T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-15-cyfrin-earnm-dropbox-v2-0
title: Prefer assignment to named return variables and remove explicit `return` statements
vuln_class: []
---

# Prefer assignment to named return variables and remove explicit `return` statements

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-15-cyfrin-earnm-dropbox-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md)_

---

**Description:** [Prefer](https://x.com/DevDacian/status/1796396988659093968) assignment to named return variables and remove explicit return statements.

This applies to most of the codebase however we provide one example of how `DropBoxFractalProtocol::_calculateAmountToClaim` could be refactored to remove the `tokens` variable and `return` statement by using a named return variable:

```solidity
  /// @return tokens The amount of Earnm tokens to claim.
  function _calculateAmountToClaim(uint256 tier, uint256 daysPassed) internal view returns (uint256 tokens) {
      if (tier == 6) tokens = TIER_6_TOKENS;
      if (tier == 5) tokens = TIER_5_TOKENS;
      if (tier == 4) tokens = TIER_4_TOKENS;
      if (tier == 3) tokens = TIER_3_TOKENS;
      if (tier == 2) tokens = TIER_2_TOKENS;
      if (tier == 1) tokens = TIER_1_TOKENS;

      // The maximum amount of tokens to claim is the total amount of tokens
      // Which is obtained after 4 years
      if (daysPassed > FOUR_YEARS_IN_DAYS) {
          tokens *= (10 ** EARNM_DECIMALS);
      }
      else {
          tokens = (tokens * (10 ** EARNM_DECIMALS)) * daysPassed / FOUR_YEARS_IN_DAYS;
      }
  }
```

**Mode:**
Fixed in commit [88c5f55](https://github.com/Earnft/dropbox-smart-contracts/commit/88c5f55d75d69aa2ba66779e27cddf47bddfac14).

**Cyfrin:** Verified.
