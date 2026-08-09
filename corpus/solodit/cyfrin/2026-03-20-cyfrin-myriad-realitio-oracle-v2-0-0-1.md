---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-20-cyfrin-myriad-realitio-oracle-v2-0-0-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-03-20T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-20-cyfrin-myriad-realitio-oracle-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-20-cyfrin-myriad-realitio-oracle-v2-0
title: '`MyriadCTFExchange::_matchOrdersSingleValidation` duplicates most of `_matchOrders`'
vuln_class: []
---

# `MyriadCTFExchange::_matchOrdersSingleValidation` duplicates most of `_matchOrders`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-20-cyfrin-myriad-realitio-oracle-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-20-cyfrin-myriad-realitio-oracle-v2.0.md)_

---

**Description:** `MyriadCTFExchange::_matchOrdersSingleValidation` is largely a copy of `_matchOrders` with two differences: the taker is pre-validated and its `filledAmounts` update is deferred to the caller. The shared logic, fee config validation, price checks, self-trade check, maker fill accounting, balance checks, match type determination, and settlement dispatch, is duplicated in full across both functions.

This increases contract size and creates a maintenance burden: any future fix or change to the settlement logic (e.g. a new match type, a balance check adjustment) must be applied in two places, with the risk of the two diverging.

**Recommended Mitigation:** Extract the shared logic into lower-level internal functions that both `_matchOrders` and `_matchOrdersSingleValidation` delegate to.



**Myriad:** Fixed in commit [`d2dec86`](https://github.com/Polkamarkets/polkamarkets-js/commit/d2dec86fbc35eaf7ac6a7db57c682461f072497c)

**Cyfrin:** Verified.
