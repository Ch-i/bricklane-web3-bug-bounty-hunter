---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-3-5
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: Consider reverting in `RebasingLibrary` functions if rounding down to zero
  occurs
vuln_class: []
---

# Consider reverting in `RebasingLibrary` functions if rounding down to zero occurs

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** `RebasingLibrary` has two functions `convertTokensToShares` and `convertSharesToTokens`. If rounding down to zero occurs such that the input is non-zero but the output is zero, consider reverting as it makes little sense to continue processing at that point. For example:

* `convertTokensToShares` should revert if `_tokens > 0 && shares == 0`
* `convertSharesToTokens` should revert if `_shares > 0 && tokens == 0`

**Securitize:** Fixed in commit [60c5f92](https://github.com/securitize-io/dstoken/commit/60c5f92e4312b069d351dd08e745875fd8f60aa5) by adding this check in `convertTokensToShares`. Note that we didn't add it in `convertSharesToTokens` as that is used by functions such as `StandardToken::balanceOf`.

**Cyfrin:** Verified.
