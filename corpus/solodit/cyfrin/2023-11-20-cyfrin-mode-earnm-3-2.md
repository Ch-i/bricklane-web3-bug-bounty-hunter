---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-11-20-cyfrin-mode-earnm-3-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-11-20T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-20-cyfrin-mode-earnm.md
tags:
- firm:cyfrin
- report:2023-11-20-cyfrin-mode-earnm
title: Potential Risk of Price Volatility in EarnNM Token Due to Concentrated Mystery
  Box Rewards
vuln_class: []
---

# Potential Risk of Price Volatility in EarnNM Token Due to Concentrated Mystery Box Rewards

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-11-20-cyfrin-mode-earnm.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-20-cyfrin-mode-earnm.md)_

---

**Description:** The current mechanism for distributing mystery box rewards in the system is based on randomness, which carries the risk of a large influx of tokens entering circulation within a short span. In particular, unusual situations might arise where a substantial number of high-value boxes (such as 1 mythical, 2 legendary, and 10 epic) are allocated over a brief period, like 1-2 days. Additionally, there's a possibility of minting a significant volume of boxes in a short duration. As a result, there's a possibility that all these boxes might release EarnM tokens simultaneously when their vesting period ends.

EarnM tokens are not fee-based tokens (e.g., token value linked to protocol fees) or any staking mechanisms to encourage token retention. In effect, there are no demand drivers and no supply dampeners in the current design.

**Impact:** Intense sell pressure, especially during a market downturn, may lead to price manipulation risks in liquidity pools. Such a significant price drop could incite panic among users, prompting them to redeem their mystery boxes notwithstanding the 50/90% haircut. This action could amplify the sell-off, potentially spiralling into a severe scenario akin to previous market collapses seen with tokens like Terra Luna.

**Recommended Mitigation:** Given the uncertainty surrounding the scale and reach of EarnM token liquidity pools, we recommend the team ensures sufficient liquidity to counterbalance potential sell pressure post-vesting. Proactive liquidity management could be crucial in stabilising token value during critical periods.

**Mode:**
Acknowledged.
