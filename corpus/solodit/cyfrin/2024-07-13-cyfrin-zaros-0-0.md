---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-13-cyfrin-zaros-0-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-07-13T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md
tags:
- firm:cyfrin
- report:2024-07-13-cyfrin-zaros
title: Attacker can burn `USDToken` from any user
vuln_class: []
---

# Attacker can burn `USDToken` from any user

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-13-cyfrin.zaros.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md)_

---

**Description:** [USDToken::burn](https://github.com/zaros-labs/zaros-core-audit/blob/de09d030c780942b70f1bebcb2d245214144acd2/src/usd/USDToken.sol#L21-L24) has:
* no access control meaning anyone can call it
* arbitrary address parameter, not using `msg.sender`

**Impact:** Anyone can call `USDToken::burn` to burn the tokens of any user.

**Recommended Mitigation:** Two options:
1) implement access control such that only trusted roles can call `USDToken::burn`
2) remove the arbitrary address input and use `msg.sender` so users can only burn their own tokens

**Zaros:** Fixed in commit [819f624](https://github.com/zaros-labs/zaros-core/commit/819f624eb9fab30599bc5383191d3dcceb3c44e8).

**Cyfrin:** Verified.
