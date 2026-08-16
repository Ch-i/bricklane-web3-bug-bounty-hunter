---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-20-cyfrin-aarc-btcy-v2-0-3-8
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-02-20T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-20-cyfrin-aarc-btcy-v2-0
title: Remove redundant `whenNotPaused` modifiers
vuln_class: []
---

# Remove redundant `whenNotPaused` modifiers

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-20-cyfrin-aarc-btcy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md)_

---

**Description:** `IBTCY::transfer, transferFrom` have the `whenNotPaused` modifier however this is redundant since `_update` also has it.

**Aarc:** Fixed in commit [c3172bb](https://github.com/aarc-xyz/btcy-contracts-main/commit/c3172bbd299500df5f24a064a39e04bc29c158ca).

**Cyfrin:** Verified.
