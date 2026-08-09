---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-06-17-cyfrin-templedao-v2-1-1-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-06-17T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-06-17-cyfrin-templedao-v2.1.md
tags:
- firm:cyfrin
- report:2024-06-17-cyfrin-templedao-v2-1
title: When recoverToken in DaiGoldAction contract is called, it does not update the
  status
vuln_class: []
---

# When recoverToken in DaiGoldAction contract is called, it does not update the status

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-06-17-cyfrin-templedao-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-06-17-cyfrin-templedao-v2.1.md)_

---

**Description:** recoverToken function moves specific amount of TGLD from the auction contract to another and delete last epoch so that it can be reset and restart.
The tokens get moved but the status nextAuctionGoldAmount is not subtracted, and this gives incorrect amount of TLGD tokens to the next epoch, and as a result, the bidders won't be able to claim their TGLD.

**Impact:** The next auction has incorrect number as auction amount which results in users not being able to claim tokens after the auction ends.

**Recommended Mitigation:** The nextAuctionGoldAmount should be subtracted when tokens are moved in recoverToken function.

**TempleDAO:** Fixed in [PR 1027](https://github.com/TempleDAO/temple/pull/1027)

**Cyfrin:** Verified
