---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-02-cyfrin-evo-soulboundtoken-v2-0-0-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-06-02T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-02-cyfrin-evo-soulboundtoken-v2.0.md
tags:
- firm:cyfrin
- report:2025-06-02-cyfrin-evo-soulboundtoken-v2-0
title: Whale can buy near-infinite voting power via `mintWithTerms`
vuln_class: []
---

# Whale can buy near-infinite voting power via `mintWithTerms`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-02-cyfrin-evo-soulboundtoken-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-02-cyfrin-evo-soulboundtoken-v2.0.md)_

---

**Description:** Since whales can control near-infinite addresses, as long as they have the funds they can buy near-infinite voting power via `mintWithTerms`.

**Impact:** This could be used seconds before a proposal is due to expire to decide that proposal. Long-term impact is limited however since the admins can blacklist addresses which burn the NFTs.

**Recommended Mitigation:** Implement a snapshot mechanism to capture total and individual user voting power prior to proposals. Consider implementing pausing to prevent users from minting NFTs via `mintWithTerms` since this is the only function which allows "unlimited mints".

**Evo:**
Fixed in commit [2fbd2c5](https://github.com/contractlevel/sbt/commit/2fbd2c5379a5f07a8166ec4041f392d867f5bedd) by allowing admins to pause `mintWithTerms`.

**Cyfrin:** Verified.
