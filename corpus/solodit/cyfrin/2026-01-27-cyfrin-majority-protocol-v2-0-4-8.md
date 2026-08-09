---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-27-cyfrin-majority-protocol-v2-0-4-8
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-01-27T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-27-cyfrin-majority-protocol-v2-0
title: '`DefaultSession::assertResults` should revert if `proposedWinners`, `totalXPs`
  and `totalTimes` array lengths don''t match'
vuln_class: []
---

# `DefaultSession::assertResults` should revert if `proposedWinners`, `totalXPs` and `totalTimes` array lengths don't match

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-27-cyfrin-majority-protocol-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md)_

---

**Description:** `DefaultSession::assertResults` should revert if `proposedWinners`, `totalXPs` and `totalTimes` array lengths don't match.

**Impact:** If an asserter makes a mistake passing different length of `proposedWinners`, `totalXPs` and `totalTimes`, the asserter will loss their bond.

**Recommended Mitigation:** Check that `proposedWinners`, `totalXPs` and `totalTimes` have the same length.

**Majestic Games:**
Fixed in commit [aafd672](https://github.com/Engage-Protocol/engage-protocol/commit/aafd672a20ba8771c36a860fd8b9b59ab966a594).

**Cyfrin:** Verified.
