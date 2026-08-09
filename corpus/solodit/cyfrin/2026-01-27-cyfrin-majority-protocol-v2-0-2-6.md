---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-27-cyfrin-majority-protocol-v2-0-2-6
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-01-27T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-27-cyfrin-majority-protocol-v2-0
title: '`SPBinaryPrompt::getScore` and `getResult` conflict on what score users who
  didn''t participate should receive, `getScore` also rewards users who got the wrong
  answer'
vuln_class: []
---

# `SPBinaryPrompt::getScore` and `getResult` conflict on what score users who didn't participate should receive, `getScore` also rewards users who got the wrong answer

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-27-cyfrin-majority-protocol-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md)_

---

**Description:** `SPBinaryPrompt::getScore` returns 0 if a user didn't participate, but `getResult` calls `getScore`, and if the score is 0, returns `xpTIers[1]`.

`SPBinaryPrompt::getScore` also gives users a score based on the probability prediction even if the user chose the wrong answer, since it never checks `answerAIsWinner == reactions[questionId][player].answer`.

**Impact:** Users who didn't participate can actually get > 0 score if `xpTiers[1] > 0`. Users who didn't get the right answer still get rewarded based on their probability prediction.

**Recommended Mitigation:** Resolve the inconsistency between `SPBinaryPrompt::getScore` and `getResult`. Don't reward users who got the wrong answer.

**Majority Games:**
Fixed in commits [50657e9](https://github.com/Engage-Protocol/engage-protocol/commit/50657e94bb54245a456520c41982b882d2d08433), [a55eb19](https://github.com/Engage-Protocol/engage-protocol/commit/a55eb1998d08ebfff17e668887986878409cd8d5).

**Cyfrin:** Verified.
