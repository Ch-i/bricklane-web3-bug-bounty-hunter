---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-06-17-cyfrin-templedao-v2-1-1-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-06-17T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-06-17-cyfrin-templedao-v2.1.md
tags:
- firm:cyfrin
- report:2024-06-17-cyfrin-templedao-v2-1
title: Misconfiguration of minting TGLD leads to max supply amount being minted too
  fast
vuln_class: []
---

# Misconfiguration of minting TGLD leads to max supply amount being minted too fast

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-06-17-cyfrin-templedao-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-06-17-cyfrin-templedao-v2.1.md)_

---

**Description:** When minting TGLD through TempleGold contract, the minting amount should be larger than the minimum amount which is 10,000 TGLD. Also if it's the first time that mint happens, the mint amount is always SUPPLY * n/d, which is the amount for one second.

The math above shows that the minting amount per second should be bigger than 10,000 TGLD, which also means that the max supply(1e9 TGLD) gets minted in 1e5 seconds ~ 1day 4hrs.

**Impact:** Either max supply tokens are minted in 1day 4hrs, or tokens can't be minted for the first minting.

**Recommended Mitigation:** When TGLD contract is created or setVestingFactor is called for the first time, it should initialize `_lastMintTimestamp`.

**TempleDAO:** Fixed in [PR 1026](https://github.com/TempleDAO/temple/pull/1026)

**Cyfrin:** Verified
