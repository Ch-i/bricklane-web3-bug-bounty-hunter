---
affected_contracts: []
derives_from: []
id: solodit-guardian-audits-2022-05-23-ultimate-fantoms-0-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2022-05-23T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Guardian%20Audits/2022-05-23-Ultimate%20Fantoms.md
tags:
- firm:guardian-audits
- report:2022-05-23-ultimate-fantoms
title: UF-4 | Mint Failure
vuln_class: []
---

# UF-4 | Mint Failure

_Section severity (from Solodit section header): Medium_  
_Audit firm: Guardian Audits_  
_Source report: [2022-05-23-Ultimate Fantoms.md](https://github.com/solodit/solodit_content/blob/main/reports/Guardian%20Audits/2022-05-23-Ultimate%20Fantoms.md)_

---

**Description**

In `publicMint`, when performing `_earnTo = random() % (_tokenIdCounter.current() +1)`, there is a
possibility `_earnTo` is equivalent to `_tokenIdCounter.current()` which yields a `tokenID` for a token that
does not exist yet. Therefore, the subsequent call to `ownerOf` will fail and the mint will revert.

**Recommendation**

Perform `random() % _tokenIdCounter.current()`.

**Resolution**

Ultimate Fantoms: Resolved, applied suggestion.
