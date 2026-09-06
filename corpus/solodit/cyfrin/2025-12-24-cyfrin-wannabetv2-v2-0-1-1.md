---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-wannabetv2-v2-0-1-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-wannabetv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-wannabetv2-v2-0
title: Judge can designate arbitrary winner who is neither maker nor taker
vuln_class: []
---

# Judge can designate arbitrary winner who is neither maker nor taker

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-wannabetv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-wannabetv2-v2.0.md)_

---

**Description:** When calling `Bet::resolve`, the nominated judge can designate an arbitrary winner to receive the winnings.

**Impact:** The judge can send the winnings to themselves or to any other non-related party who didn't participate in the bet, even though the bet is a contract between the `maker` and `taker`.

**Recommended Mitigation:** `Bet::resolve` should enforce that the winner is either the `maker` or the `taker`.

**WannaBet:** Fixed in commit [74654b5](https://github.com/gskril/wannabet-v2/commit/74654b59cc63c95c5ea8dd31f1e561bf7bd66285).

**Cyfrin:** Verified.
