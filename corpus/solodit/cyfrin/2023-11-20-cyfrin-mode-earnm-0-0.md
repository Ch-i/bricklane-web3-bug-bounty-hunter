---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-11-20-cyfrin-mode-earnm-0-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-11-20T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-20-cyfrin-mode-earnm.md
tags:
- firm:cyfrin
- report:2023-11-20-cyfrin-mode-earnm
title: Polygon chain reorgs will change mystery box tiers which can be gamed by validators
vuln_class: []
---

# Polygon chain reorgs will change mystery box tiers which can be gamed by validators

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2023-11-20-cyfrin-mode-earnm.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-20-cyfrin-mode-earnm.md)_

---

**Description:** [`REQUEST_CONFIRMATIONS = 3`](https://github.com/Earnft/smart-contracts/blob/43d3a8305dd6c7325339ed35d188fe82070ee5c9/contracts/MysteryBox.sol#L26) is too small for polygon, as [chain re-orgs frequently have block-depth greater than 3](https://polygonscan.com/blocks_forked?p=1).

**Impact:** Chain re-orgs re-order blocks and transactions changing randomness results. Someone who originally won a rare box could have that result changed into a common box and vice versa due to changing randomness result during the re-org.

This can also be [exploited by validators](https://docs.chain.link/vrf/v2/security/#choose-a-safe-block-confirmation-time-which-will-vary-between-blockchains) who can intentionally rewrite the chain's history to force a randomness request into a different block, changing the randomness result. This allows validators to get a fresh random value which may be to their advantage if they are minting mystery boxes by moving the txn around to get a better randomness result to mint a rarer box.

**Recommended Mitigation:** `REQUEST_CONFIRMATIONS = 30` appears very safe for polygon as it is very rare for chain re-orgs to have block-depth greater than this. If this happens occasionally it isn't a big deal, but if it happens all the time ("3" ensures this) that is not good and potentially exploitable by validators.

**Mode:**
Fixed in commit [85b2012](https://github.com/Earnft/smart-contracts/commit/85b20121604b5d162bb14c2c96731b8345ca1cb3).

**Cyfrin:** Verified.
