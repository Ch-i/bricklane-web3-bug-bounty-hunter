---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-2-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-01-05T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-05-cyfrin-statusl2-v2-0
title: Commit-reveal does not sufficiently protect against slash frontrunnings
vuln_class: []
---

# Commit-reveal does not sufficiently protect against slash frontrunnings

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-05-cyfrin-statusl2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md)_

---

**Description:** A commit-reveal scheme in `RLN` to battle the case where a slasher frontruns another by using the provided private key, but setting up his own reward recipient address. It works in the following 2-step way:
1. Commit a hash.
2. Reveal the private key and rewards address corresponding to that hash. In step 2, the actual slash happens.

However, this protection is insufficient as instead of the usual case where the attacker would frontrun the slash directly, he can simply frontrun the reveal by seeing the private key then.

**Impact:** Frontrunning protection is insufficient.

**Recommended Mitigation:** Make `slash()` internal so only commit-reveal way of slashing is available. The other option is to only make `slash()` available to call when no commit slash has been made.

**StatusL2:** Fixed in [0644175](https://github.com/status-im/status-network-monorepo/commit/0644175caf0904af9eee182b7d4c7dc39ade9823).

**Cyfrin:** Verified.
