---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-19-cyfrin-linea-spingame-v2-0-2-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-03-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-19-cyfrin-linea-spingame-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-19-cyfrin-linea-spingame-v2-0
title: Race Condition in `updatePrizes` Leading to Unexpected Prizes
vuln_class: []
---

# Race Condition in `updatePrizes` Leading to Unexpected Prizes

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-19-cyfrin-linea-spingame-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-19-cyfrin-linea-spingame-v2.0.md)_

---

**Description:** The `updatePrizes` function allows modifying the list of available prizes. However, it does not consider ongoing participations where the randomness request has not yet been fulfilled, leaving some participants without an assigned prize ID. This means a participant can initiate a spin, and before the VRF provides the random number, the `updatePrizes` function can be called. As a result, the prize mapping is updated, causing the participant to receive a prize from a different list than the one they originally played for.

**Impact:** Participants may receive prizes from an updated list rather than the one that was active when they initially participated.

**Proof of Concept:**
1. A participant initiates a spin.
2. Before the VRF fulfills the randomness request, updatePrizes is called, modifying the prize distribution.
3. The participant then receives a prize from the updated list rather than the expected one.

**Recommended Mitigation:** Ensure that all pending VRF requests are fulfilled before allowing any updates to the prize list.

**Linea:** Acknowledged. Acceptable behavior.

**Cyfrin:** Acknowledged.
