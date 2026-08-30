---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-04-cyfrin-parallel3-1-v2-0-3-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-03-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-04-cyfrin-parallel3-1-v2-0
title: Consider making `globalCreditLimit` an `int256`
vuln_class: []
---

# Consider making `globalCreditLimit` an `int256`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-04-cyfrin-parallel3.1-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md)_

---

**Description:** `BridgeableTokenP.sol` has global limits on difference `creditedTokens  - debitedTokens`. Lowest value `globalDebitLimit` is `int256`. While highest value `globalCreditLimit` is `uint256`,  i.e. it explicitly assumes `> 0`.

It's possible that in extreme scenario you'll want to encourage leaving certain chain, so `globalCreditLimit` will be negative.

**Recommended Mitigation:** Consider making `globalCreditLimit` an `int256`.

**Parallel:** Acknowledged. The scenario described (encouraging tokens to leave a chain) is already achievable by setting `globalCreditLimit = 0` and adjusting `globalDebitLimit`.
