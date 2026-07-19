---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-27-cyfrin-majority-protocol-v2-0-4-10
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-01-27T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-27-cyfrin-majority-protocol-v2-0
title: '`Prompt::finalizedAnswer` is never set'
vuln_class: []
---

# `Prompt::finalizedAnswer` is never set

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-27-cyfrin-majority-protocol-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md)_

---

**Description:** When a game creator reveal a question the session manager checks the hash previously created and calls `revealQuestion` in the strategies. The strategy decodes  the `Prompt` and sets it in `revealedQuestions[questionId]`. Each `Prompt` struct has its own `finalizedAnswer`:
```solidity
struct Prompt {
        address sessionManager;
        uint256 gameId;
        string questionText;
        uint256 reactionDeadline;
        string finalizedAnswer;
        string[] media;
        string[] choices;
    }
```

After all votes are revealed the final answer has to be set in the `revealedQuestions[questionId].finalizedAnswer`. The problem is that no strategies are exposing a function to set this value.

**Impact:** `Prompt::finalizedAnswer` is never set after the answers are revealed; it appears to not be used at all.

**Recommended Mitigation:** Either set or remove `Prompt::finalizedAnswer`.

**Majority Games:**
Fixed in commit [581a98d](https://github.com/Engage-Protocol/engage-protocol/commit/581a98d91b0246443f5c51bde665ae3641441fd3).

**Cyfrin:** Verified.
