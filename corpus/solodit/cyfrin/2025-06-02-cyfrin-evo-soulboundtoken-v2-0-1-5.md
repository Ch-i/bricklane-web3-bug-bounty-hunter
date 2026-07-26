---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-02-cyfrin-evo-soulboundtoken-v2-0-1-5
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-06-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-02-cyfrin-evo-soulboundtoken-v2.0.md
tags:
- firm:cyfrin
- report:2025-06-02-cyfrin-evo-soulboundtoken-v2-0
title: '`else` can be omitted in `mintWithTerms`'
vuln_class: []
---

# `else` can be omitted in `mintWithTerms`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-02-cyfrin-evo-soulboundtoken-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-02-cyfrin-evo-soulboundtoken-v2.0.md)_

---

**Description:** `else` can be omitted in `mintWithTerms` since if signature validation failed a revert will occur:
```diff
        if (!_verifySignature(signature)) revert SoulBoundToken__InvalidSignature();
-       else emit SignatureVerified(msg.sender, signature);
+       emit SignatureVerified(msg.sender, signature);
        tokenId = _mintSoulBoundToken(msg.sender);
```

**Evo:**
Fixed in commit [e3b2f74](https://github.com/contractlevel/sbt/commit/e3b2f74239601b2721118e11aaa92b42dbb502e9).

**Cyfrin:** Verified.

\clearpage
