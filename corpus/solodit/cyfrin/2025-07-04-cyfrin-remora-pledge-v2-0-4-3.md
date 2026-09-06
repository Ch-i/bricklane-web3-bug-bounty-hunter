---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-4-3
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: Remove `< 0` comparison for unsigned integers
vuln_class: []
---

# Remove `< 0` comparison for unsigned integers

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** Unsigned integers can't be `< 0` so this comparison should be removed:
`PledgeManager.sol`:
```diff
-        if (numTokens <= 0 || _propertyToken.balanceOf(signer) < numTokens)
+        if (numTokens == 0 || _propertyToken.balanceOf(signer) < numTokens)
```

**Remora:** Fixed in commit [6be4660](https://github.com/remora-projects/remora-smart-contracts/commit/6be4660990ebafbb7200425978f078a0865732fe).

**Cyfrin:** Verified.
