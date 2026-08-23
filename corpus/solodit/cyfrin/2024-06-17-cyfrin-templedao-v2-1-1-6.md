---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-06-17-cyfrin-templedao-v2-1-1-6
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-06-17T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-06-17-cyfrin-templedao-v2.1.md
tags:
- firm:cyfrin
- report:2024-06-17-cyfrin-templedao-v2-1
title: No token recover mechanism when the auction ends without any bid
vuln_class: []
---

# No token recover mechanism when the auction ends without any bid

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-06-17-cyfrin-templedao-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-06-17-cyfrin-templedao-v2.1.md)_

---

**Description:** In `SpiceAuction` contract, when an auction ends with no bids, the auction tokens are locked into the contract and can't be recovered. `recoverToken` function doesn't help recover the auction token because it limits recoverable amount to `balance - totalAllocation`

**Impact:** The auction tokens can be stuck in the contract and can't be recovered, although this would be rare case.

**Recommended Mitigation:** There has to be a mechanism implemented to recover tokens from auctions when it ends without any bids.

**TempleDAO:** Fixed in [PR 1033](https://github.com/TempleDAO/temple/pull/1033)

**Cyfrin:** Verified
