---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-20-cyfrin-myriad-realitio-oracle-v2-0-0-4
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-03-20T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-20-cyfrin-myriad-realitio-oracle-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-20-cyfrin-myriad-realitio-oracle-v2-0
title: Oracle data mismatch can breaks market integrity
vuln_class: []
---

# Oracle data mismatch can breaks market integrity

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-20-cyfrin-myriad-realitio-oracle-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-20-cyfrin-myriad-realitio-oracle-v2.0.md)_

---

**Description:** The manager calls oracle `PredictionMarketV3ManagerCLOB::initialize` during market creation and during oracle updates without validating that `oracleData` matches the market configuration. The market stores `question` and `closesAt` as the values users trade against and as the time gate for resolution. The oracle uses `oracleData` to create the Reality question and its opening timestamp, which defines the resolved outcome. If `oracleData` encodes a different question or a different close time, users trade on one question and the oracle resolves a different question, or the market close time diverges from the oracle answering window.

**Recommended Mitigation:** Validate `oracleData` question and close time match stored market values before calling oracle `initialize` in market creation and oracle update.

**ByteStrike:**
Fixed in commit [`b11e9e3`](https://github.com/Polkamarkets/polkamarkets-js/commit/b11e9e38f8bb651f2b6ffa43142600524126abbc)

**Cyfrin:** Verified.

\clearpage
