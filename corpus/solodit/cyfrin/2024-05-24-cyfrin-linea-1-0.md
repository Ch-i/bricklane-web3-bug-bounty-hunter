---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-24-cyfrin-linea-1-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-05-24T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-24-cyfrin-linea.md
tags:
- firm:cyfrin
- report:2024-05-24-cyfrin-linea
title: Linea can permanently lock user ETH on L2 by censoring user transactions through
  the centralized sequencer
vuln_class: []
---

# Linea can permanently lock user ETH on L2 by censoring user transactions through the centralized sequencer

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-24-cyfrin-linea.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-24-cyfrin-linea.md)_

---

**Description:** Linea can permanently lock user ETH on L2 by censoring user transactions through the centralized sequencer; as the Linea team control the sequencer they can choose (or be forced by a government entity) to censor any users by not including their L2 transactions when building L2 blocks.

Additionally, there is no way for users to withdraw their L2 assets by [initiating an L1 transaction which would avoid the L2 censorship](https://solodit.xyz/issues/m-09-lack-of-access-to-eth-on-l2-through-l1-l2-transactions-code4rena-zksync-zksync-git).

The combination of these factors means that users bridging assets over to Linea are completely at the mercy of the Linea team for their continued freedom to transact.

This represents a significant downgrade from Ethereum's censorship resistance where even the OFAC censorship regime only had [38% enforcement](https://www.mevwatch.info) over the last 30 days.

It should be noted however that this is a common defect [[1](https://youtu.be/Y4n38NPQhrY?si=88NeDOAsyA_kgVpo&t=167), [2](https://youtu.be/e8pwv9DIojI?si=Ru4oTdy0VM7S7Hmj&t=183)] with first-generation zkEVMs and de-centralized zk L2 sequencers are an active area of research [[1](https://www.youtube.com/watch?v=nF4jTEcQbkA), [2](https://www.youtube.com/watch?v=DP84VWng2i8)], so Linea is not an exceptional case in this regard.

**Recommended Mitigation:** Migrate to a decentralized sequencer and/or implement a mechanism that would allow users to retrieve their ETH (and ideally also bridged tokens) purely by initiating an L1 transaction completely bypassing L2 censorship.

**Linea:**
Acknowledged; this will be addressed when we decentralize.
